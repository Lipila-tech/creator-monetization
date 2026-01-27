# 📋 MVP Week 1 Example Issues

This document shows how to structure issues for the first week of the 2-week sprint.

---

## **Day 1-2: Repo Setup & Authentication**

### Issue 1: `[CONFIG] Project Repository Setup & Environment Variables`
```
Labels: config, 2-week-mvp
Assignee: Peter Zyambo / Lead Dev
Priority: High

📌 Description:
Set up backend repository, dev/staging/prod environments, 
secret management (JWT secret, mobile money API keys, DB credentials).

📋 Checklist:
- [ ] Backend repo initialized (Django/Node.js)
- [ ] Environment files created (.env.example)
- [ ] JWT secret generated & stored securely
- [ ] Database connection string configured
- [ ] Redis connection configured
- [ ] CI/CD pipeline skeleton created

⏱️ Day: 1
```

---

### Issue 2: `[API-SPEC] POST /api/v1/auth/register & POST /api/v1/auth/login`
```
Labels: api-contract, high-priority, 2-week-mvp
Assignee: Integration Owner

📡 API Contract:
POST /api/v1/auth/register
POST /api/v1/auth/login

Request (Register):
{
  "email": "creator@example.com",
  "password": "secure_password",
  "full_name": "John Creator",
  "role": "creator" | "admin"
}

Success Response (200):
{
  "status": "success",
  "data": {
    "user_id": "uuid",
    "email": "creator@example.com",
    "role": "creator",
    "access_token": "jwt_token",
    "refresh_token": "refresh_jwt"
  }
}

Error Cases:
- 400: Email already exists / Validation error
- 401: Invalid credentials
- 500: Server error

✅ Checklist:
- [ ] Backend implemented & tested
- [ ] Frontend reviewed & approved
- [ ] Idempotency tested
- [ ] All error cases working
```

---

### Issue 3: `[BE] Authentication & User Models with JWT`
```
Labels: backend, high-priority, 2-week-mvp
Assignee: George Mugale (Backend)

📌 Summary:
Implement user model, JWT authentication, role-based access control.

🎯 Scope:
- [ ] User model (email, password, role, timestamps)
- [ ] Password hashing (bcrypt)
- [ ] JWT token generation & validation
- [ ] Token refresh mechanism
- [ ] Role enum (creator, admin, fan)
- [ ] Login endpoint with credentials validation
- [ ] Register endpoint with input validation

✅ Acceptance Criteria:
- [ ] Users can register with email/password
- [ ] Login returns valid JWT token
- [ ] JWT expires after 1 hour
- [ ] Refresh token extends session
- [ ] Invalid passwords rejected
- [ ] Duplicate emails prevented
- [ ] Database migrations created
- [ ] Unit tests written (80% coverage)

🧪 Testing:
- [ ] Valid registration works
- [ ] Duplicate emails rejected
- [ ] Invalid passwords fail
- [ ] JWT token can be verified
- [ ] Token expiry works
- [ ] Refresh token valid

⏱️ Day: 1-2
```

---

### Issue 4: `[FE][Lead] Login & Signup Forms`
```
Labels: frontend-lead, high-priority, 2-week-mvp
Assignee: George Mugale (Frontend)

👤 User Story:
As a creator,
I want to sign up and log in securely,
So that I can access my dashboard and receive payments.

🎨 Scope:
- [ ] Signup form (email, password, name, role selection)
- [ ] Login form (email, password)
- [ ] Form validation (email format, password strength)
- [ ] Error handling (duplicate email, wrong password)
- [ ] Loading states (form submitting spinner)
- [ ] Success → redirect to dashboard
- [ ] Token storage (localStorage with expiry check)
- [ ] Auto-logout on token expiry

🔗 API Dependencies:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- POST /api/v1/auth/refresh

✅ Acceptance Criteria:
- [ ] Signup form works with real backend
- [ ] Login form works with real backend
- [ ] Error messages clear & user-friendly
- [ ] Mobile responsive (tested on iPhone 6+)
- [ ] No console errors
- [ ] Loading states appear during submission
- [ ] Tokens stored securely
- [ ] Session persists on page reload

⏱️ Day: 1-2
```

---

### Issue 5: `[INT] Auth Flow End-to-End Testing`
```
Labels: integration, high-priority, 2-week-mvp
Assignee: Peter Zyambo (Integration Owner)

🔗 Integration Area: Authentication

📋 E2E Flow:
1. User clicks Signup
2. Fills email, password, name
3. Submits form → Backend validation
4. JWT token returned & stored
5. User redirected to dashboard
6. Token refreshes before expiry
7. Logout clears session

✅ Acceptance Criteria:
- [ ] Frontend signup calls real /api/v1/auth/register
- [ ] JWT token received & stored
- [ ] User redirected to /dashboard
- [ ] Token expiry & refresh working
- [ ] Logout clears session & localStorage
- [ ] No double-submission issues
- [ ] Error cases handled gracefully

👤 Sign-off:
- [ ] Backend endpoint is live
- [ ] Frontend tested against real API
- [ ] All error responses match spec
- [ ] Ready to merge

⏱️ Day: 2-3
```

---

## **Day 3: Creator Profiles Integration**

### Issue 6: `[API-SPEC] GET /api/v1/creators/{id} & PUT /api/v1/creators/me`
```
Labels: api-contract, high-priority, 2-week-mvp

GET /api/v1/creators/{id}
- Returns public creator profile (name, bio, avatar, follower count)
- No auth required
- Response includes payment options

PUT /api/v1/creators/me
- Requires auth (JWT)
- Creator updates own profile
- Can't update other creators' profiles
- Returns updated profile

Success Response (200):
{
  "status": "success",
  "data": {
    "id": "uuid",
    "name": "John Creator",
    "bio": "Digital artist & educator",
    "avatar_url": "https://...",
    "bank_account": "creator@bank",
    "followers": 1250,
    "earnings": 5000.00,
    "created_at": "2026-01-01T10:00:00Z"
  }
}

✅ Checklist:
- [ ] Backend implemented
- [ ] Frontend reviewed
- [ ] Authorization tested (can't edit others' profiles)
- [ ] Public access works (no auth needed for GET)
```

---

### Issue 7: `[BE] Creator Profile Model & Endpoints`
```
Labels: backend, 2-week-mvp
Assignee: George Mugale (Backend)

📌 Summary:
Implement creator profile model, public profile retrieval, 
self-profile update endpoint.

🎯 Scope:
- [ ] Creator profile model (name, bio, avatar, bank account, earnings)
- [ ] GET /api/v1/creators/{id} (public)
- [ ] PUT /api/v1/creators/me (auth required)
- [ ] Authorization: only self-edit allowed
- [ ] Bank account validation

✅ Acceptance Criteria:
- [ ] Public profile loads correctly
- [ ] Only creator can edit own profile
- [ ] Bank account fields validated
- [ ] Bio length limited (500 chars)
- [ ] Avatar URL validated
- [ ] Update returns latest profile
- [ ] No N+1 queries
- [ ] Database migration created

⏱️ Day: 3-4
```

---

### Issue 8: `[FE][Lead] Public Creator Profile Page`
```
Labels: frontend-lead, 2-week-mvp
Assignee: George Mugale (Frontend)

👤 User Story:
As a fan,
I want to see a creator's public profile,
So that I can decide to support them.

🎨 Scope:
- [ ] Creator profile page (name, bio, avatar, earnings)
- [ ] Recent transactions / supporters list (optional for MVP)
- [ ] "Pay / Support" button (links to payment page)
- [ ] Share profile link (social media)
- [ ] Loading state while fetching profile

🔗 API: GET /api/v1/creators/{id}

✅ Acceptance Criteria:
- [ ] Profile loads with real API
- [ ] Mobile responsive
- [ ] Share button works
- [ ] "Pay" button clickable
- [ ] No console errors
- [ ] 404 if creator not found

⏱️ Day: 3-4
```

---

## **Day 4-5: Wallet & Payments**

### Issue 9: `[API-SPEC] GET /api/v1/wallets/me & POST /api/v1/payments/initiate`
```
Labels: api-contract, high-priority, 2-week-mvp

GET /api/v1/wallets/me (Auth Required)
- Returns creator's wallet balance
- Includes recent transactions
- Pagination for transaction history

Response:
{
  "status": "success",
  "data": {
    "wallet_id": "uuid",
    "balance": 12500.50,
    "currency": "ZMW",
    "transactions": [
      { "id": "uuid", "amount": 500, "type": "payment", "created_at": "..." }
    ],
    "pagination": { "total": 150, "limit": 10, "offset": 0 }
  }
}

POST /api/v1/payments/initiate
- Requires auth (fan's JWT)
- Creates payment to creator
- Returns mobile money URL or response

Request:
{
  "creator_id": "uuid",
  "amount": 500.00,
  "currency": "ZMW",
  "message": "Love your content!"
}

Response:
{
  "status": "success",
  "data": {
    "payment_id": "uuid",
    "status": "pending",
    "mobile_money_url": "https://mobilemoney.provider/pay/...",
    "expires_at": "2026-01-27T11:00:00Z"
  }
}

⚠️ Idempotency:
- X-Idempotency-Key header for duplicate prevention
- 409 response if duplicate payment detected
```

---

### Issue 10: `[BE] Wallet Model & Payment Initiation`
```
Labels: backend, high-priority, 2-week-mvp
Assignee: George Mugale (Backend)

📌 Summary:
Implement immutable wallet & ledger system. 
Create payment initiation endpoint.

🎯 Scope:
- [ ] Wallet model (creator_id, balance)
- [ ] Transaction ledger model (wallet_id, amount, type, status)
- [ ] GET /api/v1/wallets/me endpoint
- [ ] POST /api/v1/payments/initiate endpoint
- [ ] Mobile money API integration (call provider)
- [ ] Idempotency handling (X-Idempotency-Key)
- [ ] Payment state machine (pending → success/failed)

✅ Acceptance Criteria:
- [ ] Wallet balance never manually edited
- [ ] All payments create ledger entries
- [ ] Ledger is immutable (append-only)
- [ ] Payment initiation calls mobile money API
- [ ] Idempotency prevents duplicate charges
- [ ] 409 response for duplicate payments
- [ ] Request timeout handling
- [ ] Database indexes on ledger (creator_id, status)

🧪 Testing:
- [ ] Get wallet returns correct balance
- [ ] Payment initiation works
- [ ] Duplicate payment returns 409
- [ ] Invalid creator returns 404
- [ ] Negative amounts rejected

⏱️ Day: 4-5
```

---

### Issue 11: `[FE][Lead] Creator Dashboard & Wallet UI`
```
Labels: frontend-lead, 2-week-mvp
Assignee: George Mugale (Frontend)

👤 User Story:
As a creator,
I want to see my wallet balance and transaction history,
So that I can track my earnings.

🎨 Scope:
- [ ] Dashboard layout (balance card, transaction list)
- [ ] Wallet balance display
- [ ] Transaction history table (date, supporter, amount, status)
- [ ] Pagination for transactions
- [ ] Refresh button to reload data
- [ ] Loading skeleton states
- [ ] Empty state (no transactions)

🔗 API: GET /api/v1/wallets/me

✅ Acceptance Criteria:
- [ ] Balance loads & updates correctly
- [ ] Transactions paginate properly
- [ ] Mobile responsive (320px+)
- [ ] Loading states appear
- [ ] Refresh works
- [ ] No console errors

⏱️ Day: 4-5
```

---

### Issue 12: `[FE][Lead] Payment Initiation UI`
```
Labels: frontend-lead, high-priority, 2-week-mvp
Assignee: George Mugale (Frontend)

👤 User Story:
As a fan,
I want to send money to a creator via mobile money,
So that I can support them directly.

🎨 Scope:
- [ ] Payment form (creator, amount, message)
- [ ] Amount validation (positive, max 999999)
- [ ] Confirmation screen (amount, fees, total)
- [ ] Mobile money redirect handling
- [ ] Success page with transaction ID
- [ ] Failure/retry page
- [ ] Loading states during payment

🔗 API: POST /api/v1/payments/initiate

✅ Acceptance Criteria:
- [ ] Form validates input
- [ ] Confirmation shows correct total
- [ ] Mobile money redirect works
- [ ] Success page displays transaction ID
- [ ] Errors handled gracefully
- [ ] No double-submission possible
- [ ] Mobile responsive

⏱️ Day: 5
```

---

## **Day 6-7: Webhooks & End-to-End Payment**

### Issue 13: `[API-SPEC] POST /api/v1/payments/webhook`
```
Labels: api-contract, high-priority, 2-week-mvp

POST /api/v1/payments/webhook (No Auth, Mobile Money Provider)

Receives payment status updates from mobile money provider.
Must be idempotent (same webhook can be received multiple times).

Request (from provider):
{
  "payment_id": "uuid",
  "status": "success" | "failed" | "pending",
  "amount": 500.00,
  "timestamp": "2026-01-27T10:30:00Z",
  "provider_transaction_id": "provider-ref-123"
}

Response (200 OK - any response code triggers retry):
{
  "status": "success",
  "message": "Webhook received"
}

⚠️ Critical:
- Duplicate webhooks must be idempotent
- Verify webhook signature (if provider supports)
- Log all webhooks for audit trail
- 200 response even if payment already processed
```

---

### Issue 14: `[BE] Payment Webhook Handler & Idempotency`
```
Labels: backend, high-priority, 2-week-mvp
Assignee: George Mugale (Backend)

📌 Summary:
Implement webhook handler for mobile money payment callbacks.
Ensure idempotency (duplicate webhooks don't double-charge).

🎯 Scope:
- [ ] POST /api/v1/payments/webhook endpoint
- [ ] Webhook signature verification
- [ ] Idempotency: check if payment already processed
- [ ] Update payment status (success/failed)
- [ ] Update creator wallet balance (success only)
- [ ] Log all webhooks for audit
- [ ] Retry mechanism for failed updates
- [ ] Dead letter queue for failed webhooks

✅ Acceptance Criteria:
- [ ] Webhook updates payment status correctly
- [ ] Duplicate webhooks don't double-charge wallet
- [ ] Wallet balance updates after success webhook
- [ ] Failed payments don't credit wallet
- [ ] Webhook signature verified
- [ ] All webhooks logged
- [ ] 200 response always returned
- [ ] Async processing (queue-based)

🧪 Testing:
- [ ] Success webhook credits wallet
- [ ] Failure webhook doesn't credit
- [ ] Duplicate webhook processed once
- [ ] Invalid signature rejected (optional)
- [ ] Missing fields rejected

⏱️ Day: 6
```

---

### Issue 15: `[INT] Full Payment Flow End-to-End`
```
Labels: integration, high-priority, 2-week-mvp
Assignee: Peter Zyambo (Integration Owner)

🔗 Integration Area: Complete Payment Flow

📋 Full E2E Flow:
1. Fan visits creator's public profile
2. Clicks "Support / Pay" button
3. Fills payment form (amount, message)
4. Sees confirmation screen
5. Clicks "Pay with Mobile Money"
6. Redirected to mobile money provider
7. Mobile money payment succeeds
8. Provider sends webhook to backend
9. Backend webhook handler updates payment status
10. Frontend detects success (polling or WebSocket)
11. Fan sees success page with transaction ID
12. Creator's wallet balance increased
13. Creator sees transaction in dashboard

✅ Acceptance Criteria:
- [ ] Payment flow completes end-to-end
- [ ] Creator wallet updates after mobile money success
- [ ] Fan sees success confirmation
- [ ] Creator sees transaction in dashboard
- [ ] Duplicate webhooks don't double-charge
- [ ] No console errors
- [ ] All error cases handled gracefully
- [ ] Response times acceptable (< 3s per step)

👤 Sign-off:
- [ ] All components working together
- [ ] Ready for production testing
- [ ] Integration owner approved

⏱️ Day: 6-7
```

---

## **Day 7-8: Payouts**

### Issue 16: `[API-SPEC] POST /api/v1/payouts/request & POST /api/v1/admin/payouts/{id}/approve`
```
Labels: api-contract, high-priority, 2-week-mvp

POST /api/v1/payouts/request (Auth Required - Creator)
- Creator requests payout to mobile money account
- Requires bank account verification
- Minimum payout amount (1000 ZMW)

Request:
{
  "amount": 5000.00,
  "bank_account": "0123456789",
  "account_name": "John Creator"
}

Response:
{
  "status": "success",
  "data": {
    "payout_id": "uuid",
    "amount": 5000.00,
    "status": "pending_approval",
    "created_at": "2026-01-27T10:00:00Z"
  }
}

POST /api/v1/admin/payouts/{id}/approve (Auth Required - Admin)
- Admin approves or rejects payout
- Triggers payment to creator's bank account

Request:
{
  "action": "approve" | "reject",
  "note": "Approved - KYC verified"
}

Response:
{
  "status": "success",
  "data": {
    "payout_id": "uuid",
    "status": "approved" | "rejected",
    "updated_at": "2026-01-27T10:30:00Z"
  }
}
```

---

### Issue 17: `[BE] Payout Request & Admin Approval`
```
Labels: backend, high-priority, 2-week-mvp
Assignee: George Mugale (Backend)

📌 Summary:
Implement payout request creation and admin approval workflow.

🎯 Scope:
- [ ] Payout model (creator_id, amount, status, bank_account)
- [ ] POST /api/v1/payouts/request endpoint
- [ ] Validation: amount <= wallet balance, min 1000 ZMW
- [ ] POST /api/v1/admin/payouts/{id}/approve endpoint
- [ ] Admin-only authorization check
- [ ] Approve: triggers payment, updates wallet
- [ ] Reject: payout marked rejected, wallet unchanged
- [ ] Wallet balance deducted on approval

✅ Acceptance Criteria:
- [ ] Creator can request payout
- [ ] Payout amount must be <= wallet balance
- [ ] Min amount enforced (1000 ZMW)
- [ ] Admin can approve/reject
- [ ] Wallet balance updated on approval
- [ ] Rejected payouts don't affect wallet
- [ ] Bank account validated (format check)
- [ ] Database migration created

⏱️ Day: 7-8
```

---

## **Day 8-10: Polish, Testing, and Go-Live**

### Issue 18: `[QA] Complete End-to-End Testing`
```
Labels: qa, go-live, high-priority, 2-week-mvp
Assignee: QA Team

🔍 Test Areas:
- [ ] Auth flow (signup, login, logout, token refresh)
- [ ] Creator profile (public viewing, self-editing)
- [ ] Payment flow (initiate, webhook, wallet update)
- [ ] Payout flow (request, admin approval)
- [ ] Admin dashboard (view transactions, approve payouts)
- [ ] Error cases (invalid input, 401, 403, 404, 500)
- [ ] Mobile responsiveness (iPhone 6+, Android)
- [ ] Browser compatibility (Chrome, Firefox, Safari)

✅ Checklist:
- [ ] All auth flows work
- [ ] Payments succeed & wallets update
- [ ] Duplicate payments prevented
- [ ] Payouts request & approval work
- [ ] Admin can see all transactions
- [ ] Mobile responsive on all pages
- [ ] No console errors/warnings
- [ ] Performance acceptable (< 3s load time)

⏱️ Day: 8-9
```

---

### Issue 19: `[QA] Production Go-Live Verification`
```
Labels: qa, go-live, high-priority, 2-week-mvp

📋 Pre-Launch Checklist:
- [ ] All critical bugs fixed
- [ ] Performance tested (load times, DB queries)
- [ ] Monitoring & alerting configured
- [ ] Backups tested & verified
- [ ] Logging working for all endpoints
- [ ] Error tracking (Sentry) configured
- [ ] Admin account created
- [ ] Support contact ready
- [ ] Mobile money production keys enabled
- [ ] Database backups scheduled

✅ Sign-off:
- [ ] **Ready for Production**
- [ ] Team confidence high (no blockers)
- [ ] Rollback plan ready

⏱️ Day: 9-10
```

---

## 📝 Notes

These examples show:
- ✅ Clear issue structure
- ✅ Specific acceptance criteria
- ✅ Dependencies between issues
- ✅ Realistic timeline
- ✅ MVP focus (what's needed to launch)

Adapt these templates to your specific needs, but maintain:
1. **API contracts first** (before implementation)
2. **Real backend integration** (no mocks)
3. **Daily backend–frontend sync** (Days 3-10)
4. **Integration owner approval** (all APIs)
5. **QA sign-off** (before deployment)

---

**Guiding Rule:** If it doesn't help a creator get paid in 2 weeks, don't add it.
