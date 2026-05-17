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
        
        # Advanced Discount Engine: Handle Percent (%) and Flat ($) types
        package_name = data.get('package')
        dtype = data.get('discount_type', 'none')
        dval = data.get('discount_value', 0)
        
        package = db.packages.find_one({"name": package_name})
        original_price = package['price'] if package else 0
        
        let_discount_amt = 0
        if dtype == 'percent':
            let_discount_amt = (original_price * dval / 100)
        elif dtype == 'flat':
            let_discount_amt = dval
            
        final_price = max(0, original_price - let_discount_amt)

        # LINKING SYSTEM: Create an automatic payment record for the new pilgrim
        db_instance.insert('payments', {
            "pilgrim_id": inserted_pilgrim.inserted_id,
            "transaction_id": f"TXN-{data['pilgrim_id']}",
            "amount_paid": final_price if data.get('status') == 'Paid' else 0,
            "payment_date": datetime.now() if data.get('status') == 'Paid' else None,
            "method": "Auto-Calculated" if data.get('status') == 'Paid' else "Pending",
            "status": data.get('status', 'Pending')
        })

        return success_response(data={"pilgrim_id": pilgrim_id, "qr_path": qr_path}, message="Pilgrim registered", status_code=201)
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
            db.payments.update_one(
                {"pilgrim_id": pilgrim['_id']},
                {"$set": {"status": data['status']}}
            )
            
            # Logic: If status is 'Paid', update the amount based on package price
            if data['status'] == 'Paid':
                package = db.packages.find_one({"name": pilgrim.get('package')})
                if package:
                    db.payments.update_one(
                        {"pilgrim_id": pilgrim['_id']},
                        {"$set": {"amount_paid": package['price'], "method": "Updated via Admin"}}
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
