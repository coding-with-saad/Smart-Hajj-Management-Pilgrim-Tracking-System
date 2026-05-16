from flask import Blueprint, render_template, request
from database.db import db
from utils.responses import success_response, error_response
from routes.auth_routes import login_required

offer_bp = Blueprint('offers', __name__)

@offer_bp.route('/offers')
@login_required
def offers_ui():
    return render_template('offers.html', active_page='offers')

@offer_bp.route('/api/offers', methods=['GET'])
@login_required
def get_offers():
    offers = [
        {
            "id": "OFFER-001",
            "title": "Ramadan Special",
            "discount": "15% OFF",
            "description": "Exclusive discount for early Ramadan bookings.",
            "valid_until": "2026-06-01"
        },
        {
            "id": "OFFER-002",
            "title": "Group Discount",
            "discount": "$500 Cashback",
            "description": "Apply if booking for more than 5 pilgrims.",
            "valid_until": "2026-08-15"
        }
    ]
    return success_response(data=offers)

@offer_bp.route('/api/offers/appeal', methods=['POST'])
@login_required
def appeal_offer():
    # Simple logic to simulate an appeal/application for a discount
    return success_response(message="Your appeal has been submitted successfully. Our team will contact you.")
