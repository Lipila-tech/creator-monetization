---
name: Backend–Frontend Integration
about: Integration task for backend and frontend alignment during MVP
title: "[INT] "
labels: ["integration", "high-priority", "2-week-mvp"]
---

## 🔗 Integration Area
What flow is being integrated?
Examples: Auth Flow, Payments, Wallet Balance, Creator Profile, Payout Request

## 📡 API Contract
**Endpoint:** `METHOD /api/v1/path`

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
- 401: Unauthorized (invalid/expired token)
- 403: Forbidden
- 500: Server error

## 🔄 End-to-End Flow
Describe the user flow being tested.
Example: User clicks Pay → Selects amount → Sees confirmation → Mobile money prompt → Success page

## ✅ Acceptance Criteria
- [ ] Frontend and backend API contract aligned
- [ ] Correct data returned from backend
- [ ] Error cases handled gracefully (user sees friendly message)
- [ ] State updates correctly (wallet, transactions, etc.)
- [ ] No double-submission issues
- [ ] Idempotency working (duplicate requests handled safely)
- [ ] All edge cases tested

## 🧪 Test Evidence
- [ ] Screenshots of working flow
- [ ] Console logs (no errors)
- [ ] Backend logs confirming correct state
- [ ] Response times acceptable (< 3s)

## 👤 Integration Owner Sign-off
**Integration Owner:** (Peter Zyambo or delegate)
- [ ] API contract approved
- [ ] Frontend is using real endpoint (not mock)
- [ ] End-to-end test passed
- [ ] Ready to merge

## ⏱️ Integration Window
Integration Days 3–5: First live integrations
Integration Days 6–7: Full end-to-end payment/payout flows
Days 9–10: Stabilization & regression testing

