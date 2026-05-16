from flask import Blueprint, jsonify, request
from database.db import db
from utils.responses import success_response, error_response
from routes.auth_routes import login_required

payment_bp = Blueprint('payments', __name__)

@payment_bp.route('/api/payments', methods=['GET'])
@login_required
def get_payments():
    # Join with pilgrim name for better display
    pipeline = [
        {
            "$lookup": {
                "from": "pilgrims",
                "localField": "pilgrim_id",
                "foreignField": "_id",
                "as": "pilgrim"
            }
        },
        {"$unwind": "$pilgrim"}
    ]
    payments = list(db.payments.aggregate(pipeline))
    
    # Format for JSON
    formatted_payments = []
    for p in payments:
        formatted_payments.append({
            "transaction_id": p.get('transaction_id'),
            "pilgrim_name": p['pilgrim']['name'],
            "amount": p.get('amount_paid', 0),
            "method": p.get('method', 'N/A'),
            "date": p.get('payment_date').strftime('%Y-%m-%d') if p.get('payment_date') else 'N/A',
            "status": p.get('status')
        })

    return success_response(data=formatted_payments)

@payment_bp.route('/api/payments', methods=['POST'])
@login_required
def create_payment():
    data = request.get_json()
    if not data or 'pilgrim_name' not in data:
        return error_response("Invalid data")
    
    # Simple search for pilgrim ID by name for the demo
    pilgrim = db.pilgrims.find_one({"name": data.get('pilgrim_name')})
    if not pilgrim:
        return error_response("Pilgrim not found", 404)

    new_payment = {
        "transaction_id": f"TXN-{pilgrim['pilgrim_id']}-{db.payments.count_documents({})+1:03d}",
        "pilgrim_id": pilgrim['_id'],
        "amount_paid": float(data.get('amount', 0)),
        "payment_date": None,
        "method": data.get('method', 'Cash'),
        "status": data.get('status', 'Paid')
    }
    
    db.payments.insert_one(new_payment)
    return success_response(message="Transaction recorded successfully", status_code=201)
