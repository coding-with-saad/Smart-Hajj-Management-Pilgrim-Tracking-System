from flask import Blueprint, request
from database.db import db, db_instance
from utils.responses import success_response, error_response
from utils.qr_generator import generate_pilgrim_qr
from routes.auth_routes import login_required
from pymongo.errors import DuplicateKeyError

pilgrim_bp = Blueprint('pilgrims', __name__)

@pilgrim_bp.route('/api/pilgrims', methods=['GET'])
@login_required
def get_pilgrims():
    pilgrims = db_instance.find('pilgrims')
    return success_response(data=pilgrims)

@pilgrim_bp.route('/api/pilgrims', methods=['POST'])
@login_required
def create_pilgrim():
    data = request.get_json()
    if not data:
        return error_response("No data provided")
    
    required_fields = ['name', 'passport', 'cnic']
    for field in required_fields:
        if field not in data or not data[field]:
            return error_response(f"Field '{field}' is required", 400)

    # Enforce String data types for core fields
    string_fields = ['name', 'passport', 'cnic', 'contact']
    for field in string_fields:
        if field in data:
            data[field] = str(data[field])

    # Validate package existence if provided
    if 'package' in data:
        package = db_instance.find_one('packages', {"name": data['package']})
        if not package:
            return error_response(f"Package '{data['package']}' does not exist", 400)

    count = db.pilgrims.count_documents({})
    pilgrim_id = f"PIL-{count + 1:03d}"
    data['pilgrim_id'] = pilgrim_id
    
    # Generate QR Code
    qr_path = generate_pilgrim_qr(pilgrim_id, data)
    data['qr_path'] = qr_path
    
    # Add timestamp for reporting
    from datetime import datetime
    data['created_at'] = datetime.now()
    
    try:
        inserted_pilgrim = db_instance.insert('pilgrims', data)
        
        # --- ROBUST PRICING ENGINE ---
        package_name = data.get('package')
        dtype = data.get('discount_type', 'none')
        dval = float(data.get('discount_value', 0))
        group_size = int(data.get('group_size', 1))
        initial_deposit = float(data.get('initial_deposit', 0))
        status = data.get('status', 'Pending')
        
        # REQUIREMENT LOCK: Ramadan Special (percent) is ONLY for 1 person
        if dtype == 'percent':
            group_size = 1 # Force single person for Ramadan
            
        package = db.packages.find_one({"name": package_name})
        base_price_unit = float(package['price']) if package else 0.0
        total_before_discount = base_price_unit * group_size
        
        discount_amt = 0.0
        if dtype == 'percent':
            discount_amt = (total_before_discount * dval / 100)
        elif dtype == 'flat' or dtype == 'group':
            discount_amt = dval
            
        final_total = max(0.0, total_before_discount - discount_amt)

        print(f"DEBUG PRICING: Pkg={package_name}, Unit={base_price_unit}, GSize={group_size}, DiscType={dtype}, Final={final_total}")

        # LINKING SYSTEM: Determine actual cash received
        actual_cash = 0.0
        if status == 'Paid' or status == 'Fully Paid':
            actual_cash = final_total
        elif status == 'Partial' or status == 'Partial Payment':
            actual_cash = initial_deposit

        db_instance.insert('payments', {
            "pilgrim_id": inserted_pilgrim.inserted_id,
            "transaction_id": f"TXN-{data['pilgrim_id']}",
            "amount_paid": actual_cash,
            "payment_date": datetime.now() if actual_cash > 0 else None,
            "method": "Initial Deposit" if status == 'Partial Payment' else "Auto-Calculated",
            "status": status
        })

        return success_response(data={"pilgrim_id": pilgrim_id, "qr_path": qr_path}, message="Pilgrim registered & linked", status_code=201)
    except DuplicateKeyError as e:
        field = "field"
        if 'cnic' in str(e): field = "CNIC"
        elif 'passport' in str(e): field = "Passport"
        elif 'pilgrim_id' in str(e): field = "Pilgrim ID"
        return error_response(f"Duplicate entry: This {field} is already registered.", 400)
    except Exception as e:
        return error_response(str(e))

@pilgrim_bp.route('/api/pilgrims/<id>', methods=['GET'])
@login_required
def get_pilgrim(id):
    pilgrim = db.pilgrims.find_one({"pilgrim_id": id}, {"_id": 0})
    if not pilgrim:
        return error_response("Pilgrim not found", 404)
    return success_response(data=pilgrim)

@pilgrim_bp.route('/api/pilgrims/<id>', methods=['PUT'])
@login_required
def update_pilgrim(id):
    data = request.get_json()
    if not data:
        return error_response("No data provided")
    
    # Update the pilgrim record
    result = db.pilgrims.update_one({"pilgrim_id": id}, {"$set": data})
    
    # If the status was updated, synchronize it with the payments collection
    if 'status' in data:
        pilgrim = db.pilgrims.find_one({"pilgrim_id": id})
        if pilgrim:
            status = data['status']
            update_fields = {"status": status}
            
            # Logic: If status is 'Paid', update the amount based on package price
            if status == 'Paid' or status == 'Fully Paid':
                package = db.packages.find_one({"name": pilgrim.get('package')})
                if package:
                    update_fields["amount_paid"] = package['price']
                    update_fields["method"] = "Fully Paid via Admin"
            elif status == 'Partial' or status == 'Partial Payment':
                # Use provided initial deposit or keep previous
                if 'initial_deposit' in data:
                    update_fields["amount_paid"] = float(data['initial_deposit'])
                    update_fields["method"] = "Partial Deposit via Admin"

            db.payments.update_one(
                {"pilgrim_id": pilgrim['_id']},
                {"$set": update_fields}
            )

    if result.matched_count == 0:
        return error_response("Pilgrim not found", 404)
    return success_response(message="Pilgrim and Payment synchronized")

@pilgrim_bp.route('/api/pilgrims/<id>', methods=['DELETE'])
@login_required
def delete_pilgrim(id):
    # First, find the pilgrim to get their internal _id
    pilgrim = db.pilgrims.find_one({"pilgrim_id": id})
    if not pilgrim:
        return error_response("Pilgrim not found", 404)

    # Delete the linked payment record first
    db.payments.delete_one({"pilgrim_id": pilgrim['_id']})
    
    # Delete the pilgrim record
    result = db.pilgrims.delete_one({"pilgrim_id": id})
    
    # Optional: Delete the QR code file to save space
    if 'qr_path' in pilgrim and pilgrim['qr_path']:
        try:
            import os
            # Remove leading slash if present for os.path
            file_path = pilgrim['qr_path'].lstrip('/')
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass

    return success_response(message="Pilgrim and financial records deleted successfully")
