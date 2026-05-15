# Research: Backend Development Patterns

## Decision: Flask Blueprints for Modular Routing
**Rationale**: Flask Blueprints allow for a clean separation of concerns. By dividing the application into auth, pilgrims, packages, and payments modules, we keep the `app.py` file lightweight and ensure that each module is independently maintainable.
**Alternatives Considered**: Single-file routing (rejected as it becomes unmanageable), Custom routing classes (rejected as Blueprints are the standard Flask way).

## Decision: PyMongo for Database Connectivity
**Rationale**: PyMongo is the official driver for MongoDB and Python. It is lightweight, allows for direct control over NoSQL queries, and is perfect for an academic project where understanding the database layer is key.
**Alternatives Considered**: Flask-PyMongo (rejected as plain PyMongo is more educational and gives more control), MongoEngine (rejected as ODM overhead is unnecessary for this scale).

## Decision: Python `qrcode` Library for ID Generation
**Rationale**: The `qrcode` library is simple, well-documented, and generates high-quality images. It supports generating QR codes from strings (URLs or Pilgrim IDs) which fits our "smart tracking" requirement perfectly.
**Alternatives Considered**: PyQRCode (good but less popular), External API generation (rejected to keep the system local and offline-capable).

## Best Practices Found
1. **Centralized DB Connection**: Implement a singleton-like pattern in `db.py` to manage the MongoDB client and connection pooling.
2. **Environment Variables**: Use `python-dotenv` to load database URIs and secret keys from a `.env` file, ensuring no sensitive data is committed to Git.
3. **Consistent Error Responses**: Create a helper function to return JSON errors in a standard format: `{"error": "message", "status": "code"}`.
4. **Input Validation**: Use standard Python dictionary checks or a lightweight library like `Marshmallow` (if scale increases) to validate incoming JSON before DB insertion.
