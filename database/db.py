import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
            cls._instance.db = cls._instance.client[os.getenv('DB_NAME', 'hajj_management')]
        return cls._instance

    @property
    def connection(self):
        return self.db

    def init_db(self):
        # Create collections if they don't exist (MongoDB does this automatically on first insert)
        # But we can add unique indexes here
        self.db.admins.create_index("username", unique=True)
        self.db.pilgrims.create_index("pilgrim_id", unique=True)
        self.db.pilgrims.create_index("cnic", unique=True)
        self.db.pilgrims.create_index("passport", unique=True)
        
        # Seed admin if none exists
        if self.db.admins.count_documents({}) == 0:
            self.db.admins.insert_one({
                "username": "admin",
                "password": "123" 
            })
            print("Default admin created.")

        # Seed packages
        if self.db.packages.count_documents({}) == 0:
            self.db.packages.insert_many([
                {"name": "Social (Low Income)", "price": 1500, "features": ["Subsidized Housing", "Shared Transport"]},
                {"name": "Economy", "price": 3000, "features": ["Standard Accommodation", "Shared Transport"]},
                {"name": "VIP", "price": 7500, "features": ["5-Star Hotel", "Private Transport"]},
                {"name": "Premium", "price": 12000, "features": ["Luxury Suite", "High-Speed Rail"]}
            ])
            print("Default packages (4) seeded.")

    # CRUD Wrappers
    def insert(self, collection, data):
        return self.db[collection].insert_one(data)

    def find(self, collection, query={}, projection={"_id": 0}):
        return list(self.db[collection].find(query, projection))

    def find_one(self, collection, query, projection={"_id": 0}):
        return self.db[collection].find_one(query, projection)

    def update(self, collection, query, data):
        return self.db[collection].update_one(query, {"$set": data})

    def delete(self, collection, query):
        return self.db[collection].delete_one(query)

db_instance = Database()
db = db_instance.connection
db_instance.init_db()
