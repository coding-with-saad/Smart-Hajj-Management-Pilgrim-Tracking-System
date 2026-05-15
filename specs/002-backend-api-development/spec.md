# Feature Specification: Backend Development

**Feature Branch**: `002-backend-api-development`  
**Created**: 2026-05-13  
**Status**: Draft  
**Input**: User description: "Backend Development Specification for Smart Hajj Management..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Admin Authentication & Session (Priority: P1)

As an administrator, I want to securely log into the management system so that I can access protected modules like pilgrim registration and financial records.

**Why this priority**: Authentication is the gatekeeper for all other administrative functions and ensures data security.

**Independent Test**: Can be tested by attempting to access `/dashboard` without logging in (should redirect or return 401) and then successfully logging in with valid credentials.

**Acceptance Scenarios**:

1. **Given** the login page, **When** the admin enters valid credentials, **Then** a session is created and the user is redirected to the dashboard.
2. **Given** a protected API endpoint, **When** accessed without an active session, **Then** the system returns a 401 Unauthorized error.

---

### User Story 2 - Pilgrim Management APIs (Priority: P2)

As an admin, I want to perform CRUD operations on pilgrim records via REST APIs so that the frontend can dynamically manage data stored in the NoSQL database.

**Why this priority**: Managing pilgrim data is the primary functional purpose of the system.

**Independent Test**: Can be tested by sending POST/GET/PUT/DELETE requests to `/api/pilgrims` using Postman and verifying the data in MongoDB Compass.

**Acceptance Scenarios**:

1. **Given** a new pilgrim's details, **When** a POST request is sent to the API, **Then** the record is successfully stored in MongoDB.
2. **Given** an existing pilgrim ID, **When** a GET request is sent, **Then** the system returns the correct pilgrim data in JSON format.

---

### User Story 3 - Dashboard Analytics Aggregation (Priority: P3)

As an admin, I want the system to aggregate statistics on pilgrims, revenue, and payments so that I can view a high-level summary on the dashboard.

**Why this priority**: Analytics provide immediate business value and situational awareness.

**Independent Test**: Can be tested by calling the analytics endpoint and verifying that the counts match the actual data in the database.

**Acceptance Scenarios**:

1. **Given** multiple records in the database, **When** the statistics API is called, **Then** it returns the correct totals for "Total Pilgrims" and "Revenue".

---

### User Story 4 - QR Code Generation (Priority: P4)

As an admin, I want the system to generate a unique QR code for each pilgrim that contains their identification details so that I can provide them with a digital ID.

**Why this priority**: This is a core "smart" feature of the project.

**Independent Test**: Can be tested by registering a pilgrim and verifying that a QR code image is generated and stored correctly.

**Acceptance Scenarios**:

1. **Given** a pilgrim ID, **When** the QR generation utility is triggered, **Then** a valid QR code image is created containing the pilgrim's unique identification link.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide RESTful endpoints for CRUD operations on Pilgrims, Packages, and Payments.
- **FR-002**: Backend MUST utilize **Flask-Session** or standard Flask sessions for admin authentication management.
- **FR-003**: All API responses MUST be in **JSON** format with appropriate HTTP status codes.
- **FR-004**: Database operations MUST be performed using **PyMongo** connecting to a local MongoDB instance.
- **FR-005**: System MUST validate all incoming JSON payloads to prevent invalid or incomplete database entries.
- **FR-006**: Backend MUST implement a utility using the `qrcode` library to generate identification images for pilgrims.
- **FR-007**: System MUST separate business logic from routing by using a modular structure (controllers/services).

### Key Entities *(include if feature involves data)*

- **Admin**: Credentials and session state.
- **Pilgrim**: Name, CNIC, Passport, Contact, Blood Group, Package ID, QR Reference.
- **Package**: Name (Economy, VIP, Premium), Price, Features.
- **Payment**: Pilgrim ID, Amount Paid, Payment Date, Status (Paid, Partial, Pending).

### Edge Cases

- **Database Connection Failure**: How does the backend handle a loss of connection to MongoDB? (Default: Log error and return 500 Internal Server Error with user-friendly message).
- **Duplicate Records**: How does the system handle duplicate CNIC or Passport numbers? (Default: Validate and return 400 Bad Request with "Duplicate Entry" error).
- **Invalid Session**: How are expired sessions handled? (Default: Force redirect to login or return 401 for API calls).

### Assumptions

- **Local MongoDB**: The system assumes a MongoDB server is running on `localhost:27017`.
- **Admin Only**: Currently, only one administrator user is required (credentials can be stored in `.env`).
- **File Storage**: QR code images will be stored in the `static/images/qr/` directory.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of CRUD endpoints return valid JSON responses.
- **SC-002**: Authentication middleware successfully protects 100% of admin-only routes.
- **SC-003**: API response time for data retrieval is under 200ms on a local environment.
- **SC-004**: QR code generation takes less than 500ms per record.
- **SC-005**: Zero hardcoded credentials in the source code (use `.env`).
