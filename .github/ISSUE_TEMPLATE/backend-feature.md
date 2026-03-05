---
name: Backend Feature
about: API endpoints and backend service implementation for MVP
title: "[BE] "
labels: ["backend"]
assignees: []
---

## Feature / Service Summary
Describe what backend service or endpoint this implements and why it's critical for the MVP.

## User Story
**As a** [creator/fan/admin]
**I want to** [action]
**So that** [benefit]

## Core Components
Select what's being implemented:
- [ ] Database models & migrations
- [ ] REST API endpoint(s)
- [ ] Business logic / service layer
- [ ] Webhook handler
- [ ] Authentication / authorization
- [ ] Error handling & validation
- [ ] Logging & monitoring

## API Endpoint(s)
List endpoints being created/updated:
```
METHOD /api/v1/path
METHOD /api/v1/path2
```

## Request & Response Contract
**Request Body:**
```json
{
  "field": "type"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {}
}
```

**Error Responses:**
- 400: Validation error
- 401: Unauthorized
- 403: Forbidden
- 500: Server error

## Database Changes
- [ ] New table(s): describe structure
- [ ] Migration file created
- [ ] Indexes added (if needed)
- [ ] Data consistency ensured (no orphaned records)

## Acceptance Criteria
- [ ] Endpoint returns correct data
- [ ] Input validation works (invalid data rejected)
- [ ] Authentication required where needed
- [ ] Authorization checks in place (creators can't access others' data)
- [ ] Error messages are clear and actionable
- [ ] Webhook / callback idempotency (if applicable)
- [ ] Database migrations run without errors
- [ ] Logging captures key operations (for debugging)

## Testing
- [ ] Unit tests written (service layer)
- [ ] Integration tests written (database + endpoint)
- [ ] Manual API testing (e.g., Postman / curl)
- [ ] Edge cases tested (empty data, invalid IDs, etc.)
- [ ] Error cases tested (401, 400, 500 responses)

## Performance
- [ ] Query performance acceptable (< 500ms)
- [ ] Batch operations optimized (avoid N+1 queries)
- [ ] Database indexes in place if needed

## Security
- [ ] Sensitive data not logged
- [ ] SQL injection protected (using ORM/parameterized queries)
- [ ] Rate limiting applied (if public endpoint)
- [ ] CORS settings correct (if needed)

## MVP Sprint Timeline
Day / Week: (e.g., Day 5: Mobile money payment initiation)

## Frontend Dependencies
Which frontend features depend on this endpoint?
Link to frontend issues:

## Risks / Blockers
Anything that could delay completion?
