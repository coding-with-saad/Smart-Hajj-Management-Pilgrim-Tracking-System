# API Contract: Dashboard Data

**Endpoint**: `GET /api/dashboard/stats`
**Description**: Fetches the summary statistics for the dashboard cards.

## Request
- **Method**: GET
- **Headers**: `Accept: application/json`

## Response (200 OK)
```json
{
  "total_pilgrims": 150,
  "total_revenue": 4500000,
  "active_packages": 3,
  "payment_distribution": {
    "paid": 95,
    "partial": 30,
    "pending": 25
  }
}
```

---

# API Contract: Pilgrim Search

**Endpoint**: `GET /api/pilgrims?search={query}`
**Description**: Returns a filtered list of pilgrims.

## Response (200 OK)
```json
[
  {
    "id": "PIL-001",
    "name": "Malik Saad Khawar",
    "passport": "AB1234567",
    "package": "VIP",
    "payment_status": "Paid"
  }
]
```
