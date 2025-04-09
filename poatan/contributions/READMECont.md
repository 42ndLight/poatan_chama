# Contribution API Endpoints

## Contribution Management

### 1. Create New Contribution
**Endpoint:** `POST /contributions/new/{chama_id}/`  
**Description:** Creates a new contribution for a specific cashpool  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
    "amount": 744
}
```
**Expected Response:** `201 Created`

### 2. View Contribution Details
**Endpoint:** `GET /contributions/detail/{chama_id}/`  
**Description:** Retrieves details of a specific contribution  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Expected Response:** `200 OK`

### 3. List Cashpool Contributions
**Endpoint:** `GET /contributions/chama/{chama_id}/`  
**Description:** Retrieves all contributions for a specific cashpool  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Expected Response:** `200 OK`

### 4. Confirm Contribution
**Endpoint:** `PATCH /contributions/confirm/{contribution_id}/`  
**Description:** Confirms a pending contribution
**Restricted** User can confirm own contributions
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Expected Response:** `200 OK`

## Authentication Required
All endpoints require authentication via Bearer Token:
```http
Authorization: Bearer <access_token>
```

## Notes
- Replace `{cashpool_id}` with actual cashpool ID
- All requests require authentication
- Contribution amounts are in the local currency
- Contribution amounts are in the local currency- Contribution amounts are in the local currency




