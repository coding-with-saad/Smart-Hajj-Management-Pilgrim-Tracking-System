# Quickstart: Database Setup & Test Execution

## 1. Local MongoDB Configuration
1. Ensure **MongoDB Server** is installed and running on `localhost:27017`.
2. Open **MongoDB Compass**.
3. Connect to the local instance.
4. (Optional) Run `python database/db.py` to trigger initial collection creation and admin seeding.

## 2. Running API Tests with Postman
1. Open **Postman**.
2. Create a new Collection named "Smart Hajj API".
3. Add a `POST` request to `http://localhost:5000/api/pilgrims`.
4. Test the validation by sending the same CNIC twice.
5. Verify the "E11000 duplicate key error" is handled by the API (returns 400 instead of crashing).

## 3. Database Validation Commands
Run these in the Mongo Shell (mongosh) or Compass:
```javascript
// Check unique indexes
db.pilgrims.getIndexes()

// Verify linked payments
db.payments.find({ pilgrim_id: ObjectId("...") })
```
