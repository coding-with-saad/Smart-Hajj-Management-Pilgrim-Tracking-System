# API Contracts: Backend Development

## 1. Authentication
**POST `/api/auth/login`**
- **Input**: `{"username": "...", "password": "..."}`
- **Success (200)**: `{"message": "Login successful", "user": "admin"}`
- **Error (401)**: `{"error": "Invalid credentials"}`

## 2. Pilgrim Management
**GET `/api/pilgrims`**
- **Success (200)**: Array of Pilgrim objects.

**POST `/api/pilgrims`**
- **Input**: `{"name": "...", "passport": "...", "package_id": "...", ...}`
- **Success (201)**: `{"message": "Pilgrim registered", "pilgrim_id": "PIL-XXX"}`

**GET `/api/pilgrims/<id>`**
- **Success (200)**: Single Pilgrim object.

## 3. Dashboard Analytics
**GET `/api/dashboard/stats`**
- **Success (200)**:
  ```json
  {
    "total_pilgrims": 150,
    "total_revenue": 4500000,
    "active_packages": 3,
    "payment_distribution": { "paid": 95, "partial": 30, "pending": 25 }
  }
  ```

## 4. QR Code Utility
**GET `/api/qr/<pilgrim_id>`**
- **Success (200)**: Serves the QR image file.
- **Error (404)**: `{"error": "QR code not found"}`
