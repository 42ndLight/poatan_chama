# Cashpool API Endpoints

## Cashpool Management

### 1. Create New Cashpool
**Endpoint:** `POST /cashpool/new/`  
**Description:** Creates a new cashpool  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
    "name" : "ChamaOne",
    "chama_admin" : 7
}
```

**Expected Response:** `201 Created`

### 2. List Cashpools
**Endpoint:** `GET /cashpool/list/`  
**Description:** Retrieves all available cashpools
**Restriction:** Only Admins can view
**Headers:**
```http
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "chama_id": 3
}
```
**Expected Response:** `200 OK`

### 3. View Cashpool Details
**Endpoint:** `GET /cashpool/detail/{chama_id}/`  
**Description:** Retrieves details of a specific cashpool  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Expected Response:** `200 OK`

### 4. Update Cashpool
**Endpoint:** `PATCH /cashpool/update/{chama_id}/`  
**Description:** Updates cashpool information  
**Headers:**
```http
Authorization: Bearer <access_token>
```

pass any value as name and description to edit chama info 


**Expected Response:** `200 OK`

### 5. Join Cashpool
**Endpoint:** `POST /cashpool/join/`  
**Description:** Join an existing cashpool  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
    "chama_id": 3
}
```
**Expected Response:** `200 OK`

### 6. List Cashpool Members
**Endpoint:** `GET /cashpool/members/{chama_id}`  
**Description:** Retrieves all members of a cashpool  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Expected Response:** `200 OK`

### 7. View Specific Cashpool
**Endpoint:** `GET /cashpool/cashpool/{chama_id}/`  
**Description:** Retrieves information for a specific cashpool  
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
- Replace `{id}` in URLs with actual cashpool IDs
- All requests require authentication
- `chama_id` refers to the ID of the cashpool you want to join