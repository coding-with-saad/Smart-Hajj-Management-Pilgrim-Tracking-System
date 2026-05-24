import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def seed_data():
    client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
    db = client[os.getenv('DB_NAME', 'hajj_management')]

    # Clear existing data for a fresh demo
    db.pilgrims.delete_many({})
    db.payments.delete_many({})
    db.packages.delete_many({})

    # Seed 4 Standard Packages (Matches UI requirement)
    packages = [
        {"name": "Social (Low Income)", "price": 1500, "features": ["Subsidized Housing", "Group Transport"]},
        {"name": "Economy", "price": 3000, "features": ["Standard Azizia", "Bus Transport", "Buffet"]},
        {"name": "VIP", "price": 7500, "features": ["Haram View Hotel", "Private GMC", "Category A Mina"]},
        {"name": "Premium", "price": 12000, "features": ["Royal Suite", "Bullet Train", "Helicopter"]}
    ]
    db.packages.insert_many(packages)
    print("Seeded 4 professional packages.")

    # Seed initial Pilgrim with today's date for the report generator
    pilgrim = {
        "pilgrim_id": "PIL-001",
        "name": "Malik Saad Khawar",
        "passport": "AB1234567",
        "cnic": "12345-6789012-3",
        "package": "VIP",
        "contact": "0300-1234567",
        "status": "Paid",
        "created_at": datetime.now(),
        "group_size": 1,
        "discount_type": "none",
        "discount_value": 0
    }
    result = db.pilgrims.insert_one(pilgrim)
    
    # Seed matching Payment
    db.payments.insert_one({
        "pilgrim_id": result.inserted_id,
        "transaction_id": "TXN-PIL-001",
        "amount_paid": 7500,
        "payment_date": datetime.now(),
        "method": "Seeded Data",
        "status": "Paid"
    })
    print("Seeded initial pilgrim and payment with live timestamp.")

if __name__ == "__main__":
    seed_data()
