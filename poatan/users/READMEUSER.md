# User API Endpoints

## Authentication & User Management

### 1. Register User
**Endpoint:** `POST users/register/`  
**Description:** Creates a new user account  
**Request Body:**
```json
{
  "username": "DEVChanga",
  "email": "DevChanga@example.com",
  "password": "securePassword123",
  "first_name" : "User1",
  "last_name" : "USER",
}
```
**Expected Response:** `201 Created`

### 2. User Login
**Endpoint:** `POST users/login/`  
**Description:** Authenticates user and returns access token  
**Request Body:**
```json
{
  "username": "DEVChanga",
  "password": "securepassword123"
}
```
**Expected Response:** `200 OK`

### 3. User Logout
**Endpoint:** `POST users/logout/`  
**Description:** Invalidates the user's refresh token  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
  "refresh": "<refresh_token>"
}
```
**Expected Response:** `205 Reset Content`

### 4. View User Profile
**Endpoint:** `GET users/profile/`  
**Description:** Fetches authenticated user's profile  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Expected Response:** `200 OK`

### 5. Update User Profile
**Endpoint:** `PUT users/profile/update/`  
**Description:** Updates user profile details  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
  "username": "DEVChanga",
  "email": "DEVS@example.com",
  "phone_no": "0700000000"
}
```
**Expected Response:** `200 OK`

### 6. Change Password
**Endpoint:** `PUT users/profile/change-password/`  
**Description:** Changes user password  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
  "old_password": "securepassword123",
  "new_password": "newsecurepassword456",
  "confirm_password": "newsecurepassword456"
}
```
**Expected Response:** `200 OK`

### 7. Delete User Account
**Endpoint:** `DELETE users/profile/delete/`  
**Description:** Deletes user account  
**Headers:**
```http
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
  "password": "newsecurepassword456"
}
```
**Expected Response:** `204 No Content`

## Authentication Note
Protected routes require authentication via Bearer Token in headers:
```http
Authorization: Bearer <access_token>
```
