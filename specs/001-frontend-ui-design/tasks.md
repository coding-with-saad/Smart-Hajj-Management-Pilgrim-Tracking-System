# Tasks: Frontend & UI Design

**Input**: Design documents from `/specs/001-frontend-ui-design/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize static and templates directory structure
- [x] T002 Link Bootstrap 5 and FontAwesome CSS in base layout
- [x] T003 Create base layout template with head and footer sections in templates/base.html
- [x] T004 Initialize custom global styles in static/css/style.css

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core UI infrastructure required for all pages

**⚠️ CRITICAL**: Base layout and navigation must be completed before individual pages

- [x] T005 Implement persistent sidebar navigation shell in templates/base.html
- [x] T006 [P] Add sidebar collapse/toggle logic in static/js/main.js
- [x] T007 Implement responsive top navbar with admin profile placeholder in templates/base.html
- [x] T008 [P] Design admin login page layout in templates/login.html

**Checkpoint**: Foundation ready - main UI shell and authentication entry point complete

---

## Phase 3: User Story 1 - Dashboard Analytics & Overview (Priority: P1) 🎯 MVP

**Goal**: Create a modern, interactive dashboard with summary stats and charts.

**Independent Test**: Verify dashboard stats and Chart.js render correctly on both desktop and mobile.

- [x] T009 [US1] Create dashboard grid layout using Bootstrap cards in templates/dashboard.html
- [x] T010 [P] [US1] Implement summary cards for Pilgrims, Revenue, and Packages in templates/dashboard.html
- [x] T011 [US1] Integrate Chart.js for payment distribution visualization in static/js/dashboard.js
- [x] T012 [US1] Implement fetch logic for dashboard statistics from API in static/js/dashboard.js

**Checkpoint**: User Story 1 (MVP) is fully functional with dynamic analytics.

---

## Phase 4: User Story 2 - Pilgrim Management Interface (Priority: P2)

**Goal**: Provide a searchable, clean table interface for pilgrim data.

**Independent Test**: Verify table search filters records in real-time and registration form shows validation errors.

- [x] T013 [US2] Create pilgrim management page structure in templates/pilgrims.html
- [x] T014 [P] [US2] Build responsive pilgrim records table with Bootstrap styling in templates/pilgrims.html
- [x] T015 [US2] Implement client-side search filtering logic in static/js/pilgrims.js
- [x] T016 [P] [US2] Create pilgrim registration/edit form with Bootstrap validation UI in templates/pilgrims.html
- [x] T017 [US2] Add action buttons (Edit, Delete, QR Preview) to the table rows

**Checkpoint**: User Story 2 is functional for viewing and filtering pilgrims.

---

## Phase 5: User Story 3 - QR-Based Pilgrim Tracking (Priority: P3)

**Goal**: Implement QR code preview and printable pilgrim identification cards.

**Independent Test**: Verify QR preview page displays correctly and "Print" action removes navigation elements.

- [x] T018 [US3] Create QR details and preview page in templates/qr_details.html
- [x] T019 [P] [US3] Design printable "Pilgrim Card" layout with QR placeholder in templates/qr_details.html
- [x] T020 [US3] Implement @media print CSS rules to hide UI chrome when printing in static/css/style.css

**Checkpoint**: User Story 3 is complete, enabling physical identification generation.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final responsiveness and UI consistency improvements

- [x] T021 [P] Optimize mobile breakpoints and spacing across all templates
- [x] T022 Finalize consistent typography, colors, and iconography across the application
- [x] T023 [P] Verify all internal navigation links and sidebar active states
- [x] T024 Test and fix UI behaviors for network latency (loading states)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Must be first.
- **Foundational (Phase 2)**: Depends on Phase 1 completion.
- **User Stories (Phases 3-5)**: All depend on Phase 2 (base layout).
- **Polish (Phase 6)**: Final step after all stories are implemented.

### Parallel Opportunities

- T006 (JS) and T008 (Login HTML) can be worked on in parallel during Foundation.
- T010 (HTML cards) and T011 (JS charts) can be worked on in parallel within US1.
- Once Foundation is complete, different developers could theoretically work on US1, US2, and US3 in parallel as they touch different template files.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup + Foundational (Phase 1 & 2)
2. Complete Dashboard (Phase 3)
3. **VALIDATE**: The admin has a working dashboard shell.

### Incremental Delivery

1. Add Pilgrim List (US2) to enable data management.
2. Add QR Preview (US3) to complete the "smart" feature set.
3. Final Polish.
