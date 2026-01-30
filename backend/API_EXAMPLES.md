# API Usage Examples

This file contains practical examples for using the authentication API from different frontend frameworks.

## Frontend Environment Setup

### React (.env)
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_KEY=sk_your_api_key_from_create_api_client_command
REACT_APP_CLIENT_ID=550e8400-e29b-41d4-a716-446655440000
```

---

## CURL Examples

### 1. Register Creator

```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "creator",
    "is_active": true,
    "date_joined": "2026-01-28T10:00:00Z"
  },
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

### 3. Get Profile

```bash
curl -X GET http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "X-API-Key: sk_your_api_key"
```

### 4. Update Profile

```bash
curl -X PATCH http://localhost:8000/api/v1/auth/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith"
  }'
```

### 5. Refresh Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### 6. Change Password

```bash
curl -X POST http://localhost:8000/api/v1/auth/change-password/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "SecurePassword123!",
    "new_password": "NewPassword456!",
    "new_password2": "NewPassword456!"
  }'
```

### 7. Logout

```bash
curl -X POST http://localhost:8000/api/v1/auth/logout/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```
---

## Common Issues & Solutions

### Issue: "Invalid API Key"
**Solution**: 
- Create API client: `python manage.py create_api_client --name "My App" --type web`
- Use the returned API key in the `X-API-Key` header

### Issue: "Token has expired"
**Solution**: 
- Use refresh token endpoint to get new access token
- Implement auto-refresh in your API interceptor

### Issue: CORS errors
**Solution**: 
- Add frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`
- Restart Django server

### Issue: "User type cannot be changed"
**Solution**: 
- `user_type` is read-only in serializers
- Change via Django admin if needed for staff/admin promotion
