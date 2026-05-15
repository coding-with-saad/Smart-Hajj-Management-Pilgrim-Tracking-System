# Data Model: MongoDB Schemas

## Collection: `admins`
- `_id`: ObjectId
- `username`: String (Unique)
- `password_hash`: String (Bcrypt/PBKDF2)

## Collection: `pilgrims`
- `_id`: ObjectId
- `pilgrim_id`: String (e.g., "PIL-001", Unique)
- `name`: String
- `cnic`: String (Unique)
- `passport`: String (Unique)
- `contact`: String
- `blood_group`: String
- `package_id`: ObjectId (Ref to `packages`)
- `qr_path`: String (Path to generated image)
- `registration_date`: DateTime

## Collection: `packages`
- `_id`: ObjectId
- `name`: String ("Economy", "VIP", "Premium")
- `price`: Double
- `features`: Array of Strings

## Collection: `payments`
- `_id`: ObjectId
- `pilgrim_id`: ObjectId (Ref to `pilgrims`)
- `transaction_id`: String (Unique)
- `amount_paid`: Double
- `payment_date`: DateTime
- `status`: String ("Paid", "Partial", "Pending")

## Validation Rules
- **Pilgrims**: Name and Passport are required. CNIC must be 13 digits (for PK context).
- **Payments**: Amount must be greater than zero.
- **Packages**: Price must be positive.
