# ⚙️ Smart Hajj Management System - Backend Viva Guide (Spec #2)

## 📌 Backend Overview
The backend of this system is built as a **Modular REST API** using Python and Flask. It serves as the bridge between the professional frontend templates and the NoSQL database (MongoDB), ensuring secure data handling and automated identification generation.

---

## 🛠️ Key Implementation Details

### 1. Modular "Blueprint" Architecture
- **Separation of Concerns**: Instead of a monolithic `app.py`, the backend is divided into **Blueprints**:
    - `auth_routes.py`: Handles administrator sessions and login security.
    - `pilgrim_routes.py`: Manages all Create, Read, Update, and Delete (CRUD) operations for pilgrims.
    - `dashboard_routes.py`: Aggregates real-time statistics and analytics.
    - `qr_routes.py`: Serves generated QR identification images.
- **Scalability**: This structure allows us to add future modules (like Flight or Hotel tracking) without modifying existing code.

### 2. Database Design (NoSQL with MongoDB)
- **Engine**: Local **MongoDB** server.
- **Abstraction**: Created a centralized `Database` class in `database/db.py` using the **Singleton Pattern**. This ensures the system maintains only one active connection to the database, optimizing resource usage.
- **Data Integrity**: Implemented **Unique Indexes** on CNIC, Passport Number, and Username to prevent duplicate entries at the database level.
- **Flexible Schema**: Used NoSQL to allow for varied pilgrim data without the rigid constraints of a traditional SQL database.

### 3. Smart QR Generation Utility
- **Integration**: Integrated the `qrcode` library to automatically generate a unique QR code whenever a new pilgrim is registered.
- **Automation**: The backend handles the image creation, file naming, and directory management autonomously, providing a seamless "Smart" experience.
- **Storage**: Images are stored in a structured filesystem (`static/images/qr/`) and served via a dedicated API endpoint.

### 4. Security & Validation
- **Auth Guard**: Developed a custom `@login_required` decorator. It intercepts incoming requests and verifies the session, blocking unauthorized access to administrative data.
- **Environment Management**: Used `.env` files to store sensitive data like the **Mongo URI** and **Flask Secret Key**, following industry best practices.
- **Payload Validation**: Added logic to verify that all required fields (Name, CNIC, Passport) are present in the JSON request before attempting database insertion.

---

## 📂 Backend File Structure
```text
D:/ADBMS Project/
├── database/
│   └── db.py            # Singleton MongoDB Connection
├── routes/
│   ├── auth_routes.py    # Admin Session Logic
│   ├── pilgrim_routes.py # CRUD API Endpoints
│   └── dashboard_routes.py # Analytics Logic
├── utils/
│   ├── responses.py     # Standardized JSON Response Helpers
│   └── qr_generator.py  # QR Code Logic
└── .env                 # Environment Variables (Protected)
```

---

## 🚀 Technical Stack (Backend)
- **Language**: Python 3.12+
- **Framework**: Flask (Web Server)
- **Database Driver**: PyMongo (MongoDB Connectivity)
- **Security**: Flask-Session (State Management)
- **Utilities**: `qrcode[pil]` (Image Processing), `python-dotenv` (Configuration)

---

## 💡 Potential Backend Viva Questions & Answers

**Q1: Why did you choose MongoDB (NoSQL) over SQL?**
*A: MongoDB is highly scalable and handles unstructured data efficiently. For a Hajj system, pilgrim details can vary (different documents, medical history, etc.), and a NoSQL schema allows us to store this data flexibly without complex table joins.*

**Q2: What are Flask Blueprints and why did you use them?**
*A: Blueprints are a way to organize a Flask application into smaller, reusable components. I used them to separate Authentication, Pilgrim Management, and Analytics, making the code much cleaner and easier to debug.*

**Q3: How do you protect your API endpoints from unauthorized users?**
*A: I implemented a custom Python decorator called `@login_required`. It checks the Flask `session` object for a valid user. If the user isn't logged in, it returns a 401 Unauthorized error or redirects them to the login page.*

**Q4: How does the QR code generation work?**
*A: When a pilgrim is registered, the system takes their Unique ID and Name, passes it to the `qrcode` library, and generates a PNG image. That image is saved locally, and the file path is stored in the pilgrim's database record for the frontend to display.*

**Q5: What is the purpose of the `.env` file?**
*A: It is used to keep configuration separate from the code. It stores sensitive information like the database connection string and secret keys, ensuring they aren't hardcoded or accidentally shared in version control.*
