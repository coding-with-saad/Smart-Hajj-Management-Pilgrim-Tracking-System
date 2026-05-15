from flask import Blueprint
from database.db import db
from utils.responses import success_response
from routes.auth_routes import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_stats():
    total_pilgrims = db.pilgrims.count_documents({})
    
    # Simple aggregation for revenue (assuming some mock logic for now)
    # In real app, sum up payments
    total_revenue = 0
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$amount_paid"}}}
    ]
    payment_stats = list(db.payments.aggregate(pipeline))
    if payment_stats:
        total_revenue = payment_stats[0]['total']

    stats = {
        "total_pilgrims": total_pilgrims,
        "total_revenue": total_revenue,
        "active_packages": db.packages.count_documents({}),
        "payment_distribution": {
            "paid": db.payments.count_documents({"status": "Paid"}),
            "partial": db.payments.count_documents({"status": "Partial"}),
            "pending": db.payments.count_documents({"status": "Pending"})
        }
    }
    return success_response(data=stats)
