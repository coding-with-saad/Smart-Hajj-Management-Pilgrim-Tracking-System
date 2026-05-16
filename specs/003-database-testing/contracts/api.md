# API Contract: Data Integrity & Validation

## CRUD Validation Rules

### POST /api/pilgrims
**Integrity Checks**:
- **Unique**: `passport`, `cnic`.
- **Reference**: `package` must exist in `packages`.
- **Response**: 400 if duplicate, 201 if valid.

### PUT /api/pilgrims/<id>
**Integrity Checks**:
- **Consistency**: Updating `status` in pilgrim record must reflect in the linked `payments` document.
- **Lock**: `pilgrim_id` cannot be modified after creation.

## Testing Scenarios

### TC-001: Duplicate Record Prevention
1. Submit POST with `cnic: 12345`.
2. Submit second POST with `cnic: 12345`.
3. **Expected**: System rejects second submission with 400 Bad Request.

### TC-002: Statistics Consistency
1. Fetch `GET /api/dashboard/stats`.
2. Register new pilgrim with $3000 paid.
3. Fetch `GET /api/dashboard/stats` again.
4. **Expected**: `total_revenue` increases exactly by 3000.
