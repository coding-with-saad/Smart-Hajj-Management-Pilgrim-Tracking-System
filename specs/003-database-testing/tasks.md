# Tasks: Database & Testing

**Input**: Design documents from `/specs/003-database-testing/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Phase 1: Setup (Project Initialization)

**Purpose**: Database connectivity and dependency verification

- [x] T001 Verify MongoDB server is running on localhost:27017
- [x] T002 Verify PyMongo and python-dotenv installation in environment
- [x] T003 [P] Configure MONGO_URI and DB_NAME in .env

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database logic and structure required for all modules

- [x] T004 Implement Singleton Database class in database/db.py
- [x] T005 Create unique indexes for pilgrim_id, cnic, and passport in database/db.py
- [x] T006 [P] Implement initial admin user seeding logic in database/db.py

**Checkpoint**: Database layer is initialized and unique constraints are enforced.

---

## Phase 3: User Story 1 - Database Connectivity & Core Collections (Priority: P1)

**Goal**: Establish stable connection and create core collections.

**Independent Test**: Verify via MongoDB Compass that 'pilgrims', 'packages', 'payments', and 'admins' collections exist after app startup.

- [x] T007 [US1] Implement init_db() function to create core collections in database/db.py
- [x] T008 [P] [US1] Add connection logging to verify successful MongoDB link in database/db.py

**Checkpoint**: Core collections are automatically created and verified.

---

## Phase 4: User Story 2 - Comprehensive Data Persistence (Priority: P2)

**Goal**: Enable reliable CRUD operations for all entities.

**Independent Test**: Successfully insert, retrieve, update, and delete a test record using MongoDB Compass.

- [x] T009 [US2] Implement insert_one wrapper with error handling in database/db.py
- [x] T010 [P] [US2] Implement find and find_one wrappers in database/db.py
- [x] T011 [US2] Implement update_one logic with synchronization between collections in routes/pilgrim_routes.py
- [x] T012 [P] [US2] Implement delete_one logic for record cleanup in routes/pilgrim_routes.py

**Checkpoint**: Data lifecycle management is fully functional and stable.

---

## Phase 5: User Story 3 - Data Integrity & Validation (Priority: P3)

**Goal**: Prevent duplicate or corrupted data entry.

**Independent Test**: Attempting to register two pilgrims with the same CNIC returns a 400 error.

- [x] T013 [US3] Implement server-side payload validation for required fields in routes/pilgrim_routes.py
- [x] T014 [P] [US3] Add try-catch block for DuplicateKeyError (E11000) in routes/pilgrim_routes.py
- [x] T015 [US3] Validate package_id reference existence before pilgrim insertion in routes/pilgrim_routes.py

**Checkpoint**: System rejects invalid or duplicate data entries.

---

## Phase 6: User Story 4 - Automated Reliability Testing (Priority: P4)

**Goal**: Verify system stability via standardized test suites.

**Independent Test**: 100% pass rate in Postman Collection tests.

- [x] T016 [US4] Create "Smart Hajj API" collection in Postman
- [x] T017 [P] [US4] Define negative test cases for duplicate CNIC/Passport in Postman
- [x] T018 [US4] Implement aggregation query tests for dashboard statistics in routes/dashboard_routes.py

**Checkpoint**: Entire backend workflow is validated and verified for presentation.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final data cleanup and optimization

- [x] T019 [P] Optimize database query projection to hide sensitive fields (like password_hash)
- [x] T020 Finalize database seeding script for the viva demo in tests/database_seed.py
- [x] T021 [P] Verify statistics accuracy against raw collection counts

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Prerequisite for all database work.
- **Foundational (Phase 2)**: Prerequisite for all User Stories.
- **User Story 1**: Must be first to create the schema.
- **User Story 2 & 3**: Core functional implementation.
- **User Story 4**: Final validation phase.

### Parallel Opportunities

- T003 (.env) and T006 (Admin seeding) can be done in parallel.
- T010 (Find) and T012 (Delete) logic implementation are independent.
- Postman test case definition (T017) can start as soon as endpoints are defined.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Phase 1 & 2 (Setup & Indexes).
2. Complete US1 (Collections).
3. Complete US2 (CRUD).
4. **VALIDATE**: The system can store and retrieve pilgrim data reliably.

### Incremental Delivery

1. Add US3 (Validation) to harden the system against user errors.
2. Add US4 (Postman Testing) to ensure reliability for the presentation.
3. Final Polish.
