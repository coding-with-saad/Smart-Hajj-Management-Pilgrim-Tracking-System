# Quickstart: Running the Backend APIs

## 1. Environment Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
2. Install dependencies:
   ```bash
   pip install flask pymongo qrcode[pil] python-dotenv
   ```
3. Create a `.env` file in the project root:
   ```text
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=hajj_management
   SECRET_KEY=your_secret_key_here
   ```

## 2. Running the Application
Run the Flask server:
```bash
python app.py
```
The server will start at `http://127.0.0.1:5000/`.

## 3. Testing with Postman
- **Login**: `POST /api/auth/login` with JSON body.
- **Get Pilgrims**: `GET /api/pilgrims`.
- **Generate QR**: Register a pilgrim to trigger automatic QR generation in `static/images/qr/`.

## 4. Database Debugging
Use **MongoDB Compass** to connect to `mongodb://localhost:27017` and inspect the `hajj_management` database collections (`pilgrims`, `admins`, `packages`, `payments`).
