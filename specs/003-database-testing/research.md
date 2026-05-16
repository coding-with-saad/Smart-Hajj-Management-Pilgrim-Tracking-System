# Research: NoSQL Modeling & Testing Patterns

## Decision: Hybrid Referenced Data Model
**Rationale**: For the Smart Hajj System, using referenced collections for `pilgrims` → `packages` and `payments` → `pilgrims` is the most scalable approach. While MongoDB supports embedding, referenced models allow for easier independent updates to packages (e.g., price changes) and payments without duplicating large pilgrim documents.
**Alternatives considered**: 
- **Fully Embedded**: (Rejected) Updating a package title would require scanning every pilgrim record.
- **Relational (SQL)**: (Rejected) MongoDB chosen as project constraint for flexible schema support.

## Decision: Postman for Functional API Testing
**Rationale**: Postman provides a user-friendly interface for students to demonstrate API functionality during a viva. It allows for creating reusable collections that "prove" the system works without writing complex Python-based unit tests.
**Alternatives considered**:
- **Pytest/Unittest**: (Rejected) Higher complexity for undergraduate level; less visual for presentation.

## Decision: Unique Identification Constraints
**Rationale**: To prevent the duplicate record issues encountered previously, unique indexes MUST be enforced in MongoDB on `pilgrim_id`, `cnic`, and `passport`.
**Best practices**:
- Use `create_index(..., unique=True)` in the database initialization phase.

## Decision: QR Code Linking via Identifier
**Rationale**: QR codes will encode the `pilgrim_id`. The backend will resolve this ID to fetch the full record. This keeps the QR code simple and the data link robust.
**Alternatives considered**:
- **Encoding full JSON in QR**: (Rejected) Makes QR codes too dense and hard to scan.
