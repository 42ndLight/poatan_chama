# Payout API Endpoints

## Payout Management

### 1. List All Payouts
**Endpoint:** `GET /payout/`  
**Description:** Retrieves all payouts  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Expected Response:** `200 OK`

### 2. Create Payout
**Endpoint:** `POST /payout/`  
**Description:** Creates a new payout request  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
    "amount": 500,
    "recipient": 7,
    "cashpool": 4
}
```
**Expected Response:** `201 Created`

### 3. Process Payout
**Endpoint:** `PATCH /payout/{payout_id}/process/`  
**Description:** Process a payout request (approve/reject)  
**Restricted** Only a chama admin can confirm a payout for now 
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
    "action": "approve"
}
```
**Expected Response:** `200 OK`

## Notes
- All endpoints require authentication
- `recipient` field refers to the user ID of the payout recipient
- `cashpool` field refers to the ID of the associated cash pool
- `action` can be either "approve" or "reject"
- Payout ID in the process endpoint should be replaced with actual payout ID

## Authentication Required
All endpoints require authentication via Bearer Token:
```http
Authorization: Bearer <access_token>
```