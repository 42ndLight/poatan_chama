# Ledger System Documentation

## Overview
The ledger system records financial transactions and reports balances for users and chamas, tracking deposits, withdrawals, and other transaction types.

## API Endpoint
Access ledger data via:

```
GET http://127.0.01:8000/transactions/
```

### Query Parameters
- **chama**: (Required) Chama ID.
- **user**: (Optional) User ID.
- **start_date**, **end_date**: (Optional) Date range in `YYYY-MM-DD` format.

### Example Request
Fetch deposit transactions for user `3` in chama `1` for 2024:
```
GET http://127.0.01:8000/transactions/?chama=1&user=1
```

## Responsibilities
- Record transactions (deposits, withdrawals, transfers).
- Report balances for users and chamas.
- Enable filtering by type, user, chama, and date.
- Ensure data accuracy and security.
