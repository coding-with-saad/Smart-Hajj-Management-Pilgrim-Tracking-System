# Data Model: Frontend State & Mock Objects

## UI State (Client-Side)
- `currentSidebarState`: `open` | `collapsed`
- `activeModule`: `dashboard` | `pilgrims` | `packages` | `payments`
- `searchFilter`: String (applied to pilgrim table)
- `isLoading`: Boolean

## Mock Objects (For UI Development)

### Dashboard Stats
```json
{
  "totalPilgrims": 150,
  "totalRevenue": 4500000,
  "activePackages": 3,
  "pendingPayments": 12
}
```

### Chart Data (Payment Status)
```json
{
  "labels": ["Paid", "Partial", "Pending"],
  "datasets": [{
    "data": [95, 30, 25],
    "backgroundColor": ["#198754", "#ffc107", "#dc3545"]
  }]
}
```

### Pilgrim Record
```json
{
  "id": "PIL-001",
  "name": "Malik Saad Khawar",
  "passport": "AB1234567",
  "package": "VIP",
  "paymentStatus": "Paid",
  "qr_url": "/static/images/qr/PIL-001.png"
}
```
