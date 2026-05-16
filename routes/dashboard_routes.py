from flask import Blueprint
from database.db import db
from utils.responses import success_response
from routes.auth_routes import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/api/dashboard/stats', methods=['GET'])
@login_required
def get_stats():
    # 1. Total Registered Pilgrims (Actual Count)
    total_registered = db.pilgrims.count_documents({})
    
    # 2. Total Revenue (ACTUAL SUM calculation from payments collection)
    pipeline = [
        {"$group": {"_id": None, "total": {"$sum": "$amount_paid"}}}
    ]
    revenue_data = list(db.payments.aggregate(pipeline))
    total_revenue = revenue_data[0]['total'] if revenue_data else 0
    
    # 3. Pending/Partial Payments (Count for the dashboard badge)
    total_pending = db.payments.count_documents({"status": {"$in": ["Pending", "Partial", "Payment Pending", "Partial Payment"]}})

    stats = {
        "total_pilgrims": total_registered,
        "total_revenue": total_revenue, # Real money sum now
        "active_packages": db.packages.count_documents({}),
        "payment_distribution": {
            "paid": db.payments.count_documents({"status": {"$in": ["Paid", "Fully Paid"]}}),
            "partial": db.payments.count_documents({"status": {"$in": ["Partial", "Partial Payment"]}}),
            "pending": db.payments.count_documents({"status": {"$in": ["Pending", "Payment Pending"]}})
        }
    }
    return success_response(data=stats)
