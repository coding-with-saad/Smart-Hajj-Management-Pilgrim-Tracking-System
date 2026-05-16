# Data Model: Smart Hajj Management

## Collection: pilgrims
| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| pilgrim_id | String | Unique | Internal system ID (e.g., PIL-001) |
| name | String | Required | Full name of the pilgrim |
| passport | String | Unique | Passport number |
| cnic | String | Unique | National ID number |
| package_id | ObjectId | Reference | Link to `packages` collection |
| contact | String | Required | Mobile/Phone number |
| qr_path | String | Optional | Local path to the generated QR image |

## Collection: packages
| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| name | String | Unique | Tier name (Economy, VIP, Premium) |
| price | Number | > 0 | Cost of the package |
| features | Array | - | List of services included |

## Collection: payments
| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| transaction_id | String | Unique | Internal reference (TXN-PIL-XXX) |
| pilgrim_id | ObjectId | Reference | Link to the specific pilgrim document |
| amount_paid | Number | >= 0 | Amount processed so far |
| status | String | Enum | "Paid", "Partial", "Pending" |
| method | String | - | Payment channel (Bank, Cash, etc.) |

## State Transitions
1. **Pilgrim Registration**: 
   - New `pilgrim` created.
   - Automatic `payment` initialized as "Pending".
   - `qr_path` generated.
2. **Payment Update**:
   - `amount_paid` increased.
   - `status` transitions to "Partial" or "Paid".
