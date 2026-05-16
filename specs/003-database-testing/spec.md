# Feature Specification: Database & Testing

**Feature Branch**: `003-database-testing`  
**Created**: 2026-05-15  
**Status**: Draft  
**Input**: User description: "Database & Testing Specification for Smart Hajj Management..."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Database Connectivity & Core Collections (Priority: P1)

As a system, I want to establish a stable connection to the local MongoDB server and initialize the required collections (Pilgrims, Packages, Payments, Admins) so that the application has a reliable place to store and manage data.

**Why this priority**: The database is the foundation of the entire system. Without connectivity and basic storage structure, no other features can function.

**Independent Test**: Can be fully tested by starting the Flask server and verifying (via logs or MongoDB Compass) that a connection is established and the four core collections are present.

**Acceptance Scenarios**:

1. **Given** the MongoDB server is running locally, **When** the application starts, **Then** a successful connection is logged.
2. **Given** a new database instance, **When** initialized, **Then** the 'pilgrims', 'packages', 'payments', and 'admins' collections are created.

---

### User Story 2 - Comprehensive Data Persistence (Priority: P2)

As an admin, I want to perform CRUD (Create, Read, Update, Delete) operations on pilgrim and package records so that I can maintain accurate and up-to-date information for the agency.

**Why this priority**: Managing the lifecycle of data is the primary business value of the backend system.

**Independent Test**: Can be tested by inserting a record via an API call, retrieving it, updating a field, and finally deleting it, verifying each state in MongoDB Compass.

**Acceptance Scenarios**:

1. **Given** valid pilgrim data, **When** an insert operation is triggered, **Then** the record is stored with a unique identifier.
2. **Given** an existing record ID, **When** a delete request is made, **Then** the record is permanently removed from the collection.

---

### User Story 3 - Data Integrity & Validation (Priority: P3)

As a system, I want to validate all incoming data against predefined rules before it is inserted into the database so that we prevent duplicate records (like duplicate CNICs) or corrupted data.

**Why this priority**: Prevents common database errors and ensures the system remains reliable and trustworthy during presentation.

**Independent Test**: Can be tested by attempting to insert a duplicate CNIC or a record with missing mandatory fields and verifying that the database/API rejects the operation.

**Acceptance Scenarios**:

1. **Given** a record with a CNIC that already exists, **When** insertion is attempted, **Then** the system returns a validation error.
2. **Given** a record missing a required field (e.g., Name), **When** submitted, **Then** the system prevents insertion.

---

### User Story 4 - Automated Reliability Testing (Priority: P4)

As a developer, I want to run a suite of tests (Postman or unit tests) that verify API responses and database state so that I can confidently demonstrate a stable system during the viva.

**Why this priority**: Ensures the "Smart" part of the system is robust and ready for examination.

**Independent Test**: Can be tested by running a test script that executes all major API paths and reports a "PASS" for every successful operation.

**Acceptance Scenarios**:

1. **Given** the test suite is executed, **When** all APIs are called, **Then** 100% of functional tests return a success status.

### Edge Cases

- **Server Offline**: What happens when the MongoDB service is stopped while the app is running? (Default: The app should catch the connection exception and return a 500 error).
- **Network Latency**: How does the system handle slow local disk I/O? (Default: Ensure operations are performed with reasonable timeouts).
- **Corrupted Data**: How does the system handle records that don't match the expected schema? (Default: Validation logic should skip or flag such records during retrieval).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST connect to a local MongoDB instance on port 27017.
- **FR-002**: System MUST maintain four distinct collections: `pilgrims`, `packages`, `payments`, and `admins`.
- **FR-003**: System MUST enforce unique constraints on `pilgrim_id`, `cnic`, and `passport` fields.
- **FR-004**: System MUST perform server-side validation on all JSON payloads before database commit.
- **FR-005**: All database operations MUST return standardized success/error codes to the API layer.
- **FR-006**: System MUST support aggregation queries for dashboard statistics (e.g., total revenue).

### Key Entities *(include if feature involves data)*

- **Pilgrim Collection**: Primary store for personal and identification data.
- **Package Collection**: Store for Hajj service tiers and pricing.
- **Payment Collection**: Transaction logs linked to Pilgrim IDs.
- **Admin Collection**: Credentials for system access.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Database connection is established in under 1 second during startup.
- **SC-002**: 100% of CRUD operations successfully persist data to the local disk.
- **SC-003**: Zero duplicate records allowed for primary identification fields (CNIC/Passport).
- **SC-004**: Dashboard statistics accurately reflect the sum of records in 100% of test cases.
- **SC-005**: API testing suite (Postman) achieves 100% pass rate on core functionality.
