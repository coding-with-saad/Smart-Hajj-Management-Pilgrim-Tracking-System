# Tasks: Backend Development

**Input**: Design documents from `/specs/002-backend-api-development/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Install dependencies (flask, pymongo, qrcode, python-dotenv)
- [x] T002 Create .env file with MONGO_URI and SECRET_KEY in repository root
- [x] T003 Initialize MongoDB connection utility in database/db.py
- [x] T004 Setup main app entry point with Blueprint skeleton in app.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required for all APIs

- [x] T005 Implement common JSON response helper in utils/responses.py
- [x] T006 [P] Create initial database collections (admins, packages) in database/db.py
- [x] T007 Implement basic session-based authentication protection decorator in routes/auth_routes.py

**Checkpoint**: Foundation ready - DB connected and modular structure initialized.

---

## Phase 3: User Story 1 - Admin Authentication & Session (Priority: P1)

**Goal**: Secure administrator access to the system.

**Independent Test**: Verify login API returns 200 for valid credentials and 401 for invalid ones using Postman.

- [x] T008 [US1] Implement admin login endpoint in routes/auth_routes.py
- [x] T009 [P] [US1] Create session management logic (session['user']) in routes/auth_routes.py
- [x] T010 [US1] Implement logout endpoint in routes/auth_routes.py

**Checkpoint**: Admin can log in/out and session state is maintained.

---

## Phase 4: User Story 2 - Pilgrim Management APIs (Priority: P2)

**Goal**: Full CRUD operations for pilgrim records.

**Independent Test**: Successfully create, read, update, and delete a pilgrim record via Postman.

- [x] T011 [US2] Implement GET /api/pilgrims to list all records in routes/pilgrim_routes.py
- [x] T012 [P] [US2] Implement POST /api/pilgrims to create new record in routes/pilgrim_routes.py
- [x] T013 [US2] Implement GET /api/pilgrims/<id> to fetch single record in routes/pilgrim_routes.py
- [x] T014 [P] [US2] Implement PUT /api/pilgrims/<id> for updates in routes/pilgrim_routes.py
- [x] T015 [US2] Implement DELETE /api/pilgrims/<id> in routes/pilgrim_routes.py

**Checkpoint**: CRUD operations for pilgrims are fully functional.

---

## Phase 5: User Story 3 - Dashboard Analytics Aggregation (Priority: P3)

**Goal**: Provide aggregated statistics for the dashboard cards.

**Independent Test**: Call stats API and verify counts match MongoDB data.

- [x] T016 [US3] Implement statistics aggregation logic in database/db.py
- [x] T017 [US3] Create GET /api/dashboard/stats endpoint in routes/dashboard_routes.py

**Checkpoint**: Dashboard APIs provide real-time statistics from MongoDB.

---

## Phase 6: User Story 4 - QR Code Generation (Priority: P4)

**Goal**: Automated generation of identification images.

**Independent Test**: Register a pilgrim and check if static/images/qr/ contains a valid .png file.

- [x] T018 [US4] Implement QR generation logic in utils/qr_generator.py
- [x] T019 [US4] Integrate QR generation into the Pilgrim POST API in routes/pilgrim_routes.py
- [x] T020 [P] [US4] Create endpoint to serve QR images securely in routes/qr_routes.py

**Checkpoint**: QR codes are generated automatically upon registration.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: API validation and stability

- [x] T021 Implement input validation for all POST/PUT payloads
- [x] T022 [P] Add global error handling for database connection drops
- [x] T023 Final API validation pass using Postman collection
- [x] T024 [P] Update README with final API endpoint documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Must be complete first.
- **Foundational (Phase 2)**: Depends on Setup.
- **US1 (Auth)**: Depends on Foundation (needed for route protection).
- **US2, US3, US4**: Depend on Foundation and Auth.
- **Polish (Final)**: Depends on all user stories.

### Parallel Opportunities

- T006 and T007 can be built in parallel.
- T012 and T014 (Pilgrim updates) can be built in parallel.
- Once Foundation is ready, US2 (Pilgrims) and US3 (Dashboard) can be worked on in parallel by different developers.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Setup Environment + DB Connection.
2. Complete Admin Login (US1).
3. Complete Pilgrim CRUD (US2).
4. **VALIDATE**: Frontend can now log in and manage data.

### Incremental Delivery

1. Add Dashboard Analytics (US3).
2. Add QR Generation (US4).
3. Final hardening and validation.
