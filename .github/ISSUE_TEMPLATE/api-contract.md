---
name: API Contract / Specification
about: Define and finalize API contracts between backend and frontend
title: "[API-SPEC] "
labels: ["api-contract", "integration", "high-priority", "2-week-mvp"]
---

## 📡 API Endpoint
**Endpoint:** `METHOD /api/v1/path`
**Purpose:** [Brief description of what this endpoint does]
**Owner (Backend):** @developer-name
**Consumer (Frontend):** @frontend-developer-name

## 🔐 Authentication & Authorization
- [ ] Authentication Required: Yes / No
- [ ] Auth Type: Bearer token (JWT) / API Key / None
- [ ] Authorization: 
  - Creators can access only their own data
  - Admins can access all data
  - Public endpoint (no auth needed)

## 📥 Request Contract

**Method:** GET | POST | PUT | DELETE | PATCH

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**URL Parameters (if any):**
- `creator_id`: UUID of creator
- `transaction_id`: UUID of transaction

**Query Parameters (if any):**
```
?status=pending&limit=20&offset=0
```

**Request Body:**
```json
{
  "field_name": "string | number | boolean",
  "nested_object": {
    "sub_field": "value"
  }
}
```

**Validation Rules:**
- `field_name`: Required, min 1 char, max 255 chars
- `amount`: Required, positive number, precision 2 decimals
- `status`: Enum: pending | success | failed

## 📤 Response Contract

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "created_at": "2026-01-27T10:30:00Z",
    "updated_at": "2026-01-27T10:30:00Z"
  },
  "message": "Optional success message"
}
```

**Paginated Response (200 OK):**
```json
{
  "status": "success",
  "data": [
    { "id": "1", "name": "Item 1" },
    { "id": "2", "name": "Item 2" }
  ],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 0,
    "has_more": true
  }
}
```

## ❌ Error Responses

**400 Bad Request** (Validation Error):
```json
{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "message": "Invalid request data",
  "errors": [
    {
      "field": "amount",
      "message": "Amount must be positive"
    }
  ]
}
```

**401 Unauthorized** (Missing/Invalid Token):
```json
{
  "status": "error",
  "error_code": "UNAUTHORIZED",
  "message": "Invalid or expired token"
}
```

**403 Forbidden** (Insufficient Permissions):
```json
{
  "status": "error",
  "error_code": "FORBIDDEN",
  "message": "You do not have permission to access this resource"
}
```

**404 Not Found**:
```json
{
  "status": "error",
  "error_code": "NOT_FOUND",
  "message": "Resource not found"
}
```

**409 Conflict** (Duplicate / Idempotency):
```json
{
  "status": "error",
  "error_code": "DUPLICATE_REQUEST",
  "message": "This payment has already been processed",
  "data": {
    "transaction_id": "existing-id"
  }
}
```

**500 Internal Server Error**:
```json
{
  "status": "error",
  "error_code": "SERVER_ERROR",
  "message": "An unexpected error occurred"
}
```

## 🔄 Idempotency (if applicable)
- **Idempotency Key Header:** `X-Idempotency-Key`
- **Usage:** Send same UUID in header to prevent duplicate payments
- **Duration:** Keys expire after 24 hours

## ⏱️ Rate Limiting
- **Limit:** 100 requests per minute per user
- **Headers Returned:**
  - `X-RateLimit-Limit: 100`
  - `X-RateLimit-Remaining: 95`
  - `X-RateLimit-Reset: 1674833400`

## 📋 Example cURL Request
```bash
curl -X POST https://api.nthanda.com/api/v1/payments/initiate \
  -H "Authorization: Bearer your_token_here" \
  -H "Content-Type: application/json" \
  -H "X-Idempotency-Key: $(uuidgen)" \
  -d '{
    "creator_id": "550e8400-e29b-41d4-a716-446655440000",
    "amount": 50.00,
    "currency": "ZMW"
  }'
```

## ✅ Contract Approval Checklist
- [ ] Backend developer implemented & tested
- [ ] Frontend developer reviewed contract
- [ ] Error cases defined & tested
- [ ] Response time acceptable (< 500ms)
- [ ] Idempotency tested (if applicable)
- [ ] Rate limiting tested
- [ ] Both teams agree on contract
- [ ] Endpoint is live and working

## 🔗 Related Issues
Link to backend and frontend implementation issues:
- Backend: #XXX
- Frontend: #YYY

## 📝 Notes
Any additional context or considerations?
