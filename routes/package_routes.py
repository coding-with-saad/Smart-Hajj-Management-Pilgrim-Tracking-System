from flask import Blueprint, jsonify
from database.db import db
from utils.responses import success_response
from routes.auth_routes import login_required

package_bp = Blueprint('packages', __name__)

@package_bp.route('/api/packages', methods=['GET'])
@login_required
def get_packages():
    # In a real app, these would be in the database
    # Let's seed them or just return them as a list
    packages = [
        {
            "id": "PKG-001",
            "name": "Economy",
            "price": 3000,
            "features": ["Standard Accommodation", "Shared Transport", "Full Meal Plan", "24/7 Support"]
        },
        {
            "id": "PKG-002",
            "name": "VIP",
            "price": 7500,
            "features": ["5-Star Hotel", "Private Transport", "VIP Tents in Mina", "Personal Guide", "Ziyarat Tours"]
        },
        {
            "id": "PKG-003",
            "name": "Premium",
            "price": 12000,
            "features": ["Luxury Suite", "Bullet Train Access", "24/7 Concierge", "Medical Specialist", "Executive Lounge"]
        }
    ]
    return success_response(data=packages)
