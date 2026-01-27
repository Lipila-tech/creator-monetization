# Nthanda Monetization App - Issue Template Guide

## 📋 Overview
This guide explains the issue templates available for the 2-week MVP sprint. Use the correct template to ensure clear communication and proper task tracking.

---

## 🏷️ Issue Templates

### **[BE] Backend Feature**
**File:** `.github/ISSUE_TEMPLATE/backend-feature.md`

**When to use:** 
- Creating new API endpoints
- Implementing database models & migrations
- Building backend services (wallet, payments, payouts, admin)
- Creating webhook handlers

**Assigned to:** Backend developer

**Key sections:**
- API endpoint contract (URL, method, request/response)
- Database changes & migrations
- Acceptance criteria & testing
- Security & performance review

**Example titles:**
- `[BE] Authentication & JWT`
- `[BE] Creator Wallet Model & Ledger`
- `[BE] Mobile Money Payment Initiation`
- `[BE] Admin Payout Approval Endpoint`

---

### **[FE][Lead] Frontend Feature (Lead)**
**File:** `.github/ISSUE_TEMPLATE/frontend-lead.md`

**When to use:**
- Core frontend features (auth screens, dashboard, payment UI)
- Major component implementation
- State management setup

**Assigned to:** George Mugale (Frontend Lead)

**Key sections:**
- User story
- API dependencies
- Responsive design requirements
- Real backend integration (no mocks)
- Lighthouse accessibility score > 80

**Example titles:**
- `[FE][Lead] Creator Dashboard Layout`
- `[FE][Lead] Payment Flow UI`
- `[FE][Lead] Payout Request Form`
- `[FE][Lead] Admin Transaction Viewer`

---

### **[FE][Support] Frontend Support**
**File:** `.github/ISSUE_TEMPLATE/frontend-support.md`

**When to use:**
- UI polish, styling, responsiveness
- Error message improvements
- Empty/loading states
- Accessibility fixes

**Assigned to:** Barnabas Mwaipaya (Frontend Support)

**Key sections:**
- UI focus (styling, responsiveness, polish)
- Design reference
- Cross-browser testing
- Mobile & desktop compatibility

**Example titles:**
- `[FE][Support] Mobile responsiveness fixes`
- `[FE][Support] Error message styling`
- `[FE][Support] Loading skeleton states`
- `[FE][Support] Dark mode toggle`

---

### **[INT] Backend–Frontend Integration**
**File:** `.github/ISSUE_TEMPLATE/integration.md`

**When to use:**
- Integrating backend API with frontend
- End-to-end flow testing
- Alignment during integration windows (Days 3–7)

**Assigned to:** Integration Owner (Peter Zyambo or delegate)

**Key sections:**
- API contract verification
- End-to-end flow description
- Test evidence (screenshots, logs)
- Integration owner sign-off

**Integration Windows:**
- **Days 3–5:** First live integrations
- **Days 6–7:** Full payment & payout flows
- **Days 9–10:** Stabilization & regression testing

**Example titles:**
- `[INT] Auth Flow Integration`
- `[INT] Payment Initiation End-to-End`
- `[INT] Wallet Balance & Transactions`
- `[INT] Payout Approval Flow`

---

### **[QA] QA / Go-Live Checklist**
**File:** `.github/ISSUE_TEMPLATE/qa-go-live.md`

**When to use:**
- Testing features before merge
- Launch readiness verification
- Final go-live checks
- Regression testing

**Assigned to:** QA / Testing team

**Key sections:**
- MVP QA checklist (auth, payments, wallet, payouts, admin)
- Browser & device testing
- Production readiness checklist

**Example titles:**
- `[QA] Payment Flow Testing`
- `[QA] Admin Dashboard Testing`
- `[QA] Production Go-Live Verification`
- `[QA] Post-Deployment Smoke Tests`

---

### **[BUG] Bug Report**
**File:** `.github/ISSUE_TEMPLATE/bug-report.md`

**When to use:**
- Any defect or broken feature
- Unexpected behavior
- Console errors or API failures

**Key sections:**
- Steps to reproduce
- Screenshots / videos
- Severity level (critical / high / medium / low)
- Technical details (console errors, API responses)
- Workaround (if available)

**Example titles:**
- `[BUG] Login form not submitting`
- `[BUG] Wallet balance not updating after payment`
- `[BUG] Admin payout list shows duplicates`
- `[BUG] Mobile responsiveness broken on iPhone SE`

---

### **[API-SPEC] API Contract / Specification**
**File:** `.github/ISSUE_TEMPLATE/api-contract.md`

**When to use:**
- Finalizing API contracts before implementation
- Documenting endpoint specifications
- Ensuring backend & frontend agreement

**Assigned to:** Integration Owner

**Key sections:**
- Request & response contract
- Error responses
- Idempotency & rate limiting
- Example cURL requests
- Contract approval checklist

**Workflow:**
1. Backend creates API contract issue
2. Frontend reviews & approves
3. Implementation begins
4. Both teams verify endpoint is live

**Example titles:**
- `[API-SPEC] POST /api/v1/payments/initiate`
- `[API-SPEC] GET /api/v1/wallets/me`
- `[API-SPEC] POST /api/v1/payouts/{id}/approve`

---

### **[DevOps] Deployment / DevOps**
**File:** `.github/ISSUE_TEMPLATE/devops.md`

**When to use:**
- Environment setup (dev / staging / prod)
- Database migrations & backups
- CI/CD pipeline configuration
- Monitoring & logging
- SSL/TLS, secrets management
- Deployment procedures

**Key sections:**
- Pre-deployment checklist
- Deployment steps & verification
- Post-deployment monitoring
- Rollback plan
- Security review

**Example titles:**
- `[DevOps] Production Database Setup`
- `[DevOps] CI/CD Pipeline Configuration`
- `[DevOps] Monitoring & Alerting Setup`
- `[DevOps] Pre-Production Deployment Checklist`

---

### **[CONFIG] Configuration & Setup**
**File:** `.github/ISSUE_TEMPLATE/config.md`

**When to use:**
- Environment variable setup
- Third-party service configuration (mobile money, Auth0)
- Feature flags
- Build configuration
- Secrets management

**Key sections:**
- Configuration type
- Sensitive data handling
- Implementation steps
- Verification checklist

**Example titles:**
- `[CONFIG] Mobile Money API Keys Setup`
- `[CONFIG] Environment Variables (Dev/Staging/Prod)`
- `[CONFIG] JWT Secret Management`
- `[CONFIG] Database Connection Configuration`

---

## 📊 2-Week MVP Sprint Overview

### **Daily Milestones**

**Backend Developer:**
- Day 1: Repo setup, environment config, auth models
- Day 2: JWT auth, role permissions
- Day 3: Creator profiles & public endpoints
- Day 4: Wallet & ledger models
- Day 5: Mobile money payment initiation
- Day 6: Webhooks & idempotency
- Day 7: Payout request & admin approval
- Day 8: Admin reconciliation endpoints
- Day 9: Bug fixes & integration fixes
- Day 10: Security review & deploy support

**Frontend Developer:**
- Day 1: Project setup, auth screens
- Day 2: Creator dashboard layout
- Day 3: Creator profile integration
- Day 4: Wallet & transaction UI
- Day 5: Payment flow UI
- Day 6: Success/failure states
- Day 7: Payout request UI
- Day 8: UI polish & responsiveness
- Day 9: Bug fixes & integration fixes
- Day 10: Production readiness

**Integration Windows:**
- **Days 3–5:** First live backend–frontend integrations
- **Days 6–7:** Full end-to-end payment & payout flows
- **Days 9–10:** Stabilization, regression testing, production smoke tests

---

## 🔗 Daily Backend–Frontend Handshake Checklist

Every integration day (3–10), teams verify:

- [ ] API endpoint contract agreed (URL, method, payload)
- [ ] Request/response example shared
- [ ] Error cases defined
- [ ] Frontend tested against real backend (not mocks)
- [ ] Issues logged and prioritized same day

**Integration Owner Role:**
- Approve API contracts before implementation
- Ensure frontend uses real backend endpoints
- Coordinate end-to-end testing
- Block merges breaking agreed API contracts

---

## 📋 Labeling Conventions

Every issue should have these labels:

**Type:**
- `backend` — Backend feature
- `frontend` — Frontend feature
- `integration` — Backend–Frontend integration
- `qa` — Testing & QA
- `devops` — Deployment & infrastructure
- `bug` — Defect report

**Priority:**
- `high-priority` — Blocks other work or go-live
- `2-week-mvp` — Required for MVP launch

**Status:**
- `frontend-lead` — George Mugale's ownership
- `frontend-support` — Barnabas's ownership
- `go-live` — Go-live readiness

---

## ✅ Definition of Done (MVP)

A feature is **done** when:

1. **Code:**
   - Implemented according to acceptance criteria
   - Tested (unit/integration tests for backend, manual + automated for frontend)
   - Code reviewed & approved
   - No console errors or warnings

2. **Integration:**
   - API contract agreed & approved
   - Frontend tested against real backend
   - End-to-end flow works
   - Integration owner sign-off

3. **Testing:**
   - QA verified on all browsers/devices
   - No regressions introduced
   - Production smoke tests pass

4. **Documentation:**
   - API contract documented
   - Deployment instructions clear
   - Known limitations documented

---

## 🚀 Creating Issues

### Step 1: Choose the Right Template
Select based on what you're building (backend, frontend, integration, testing, etc.).

### Step 2: Fill in Key Sections
- **Title:** Clear & specific (e.g., `[BE] Payment Webhook Handler`)
- **Labels:** Type + priority + 2-week-mvp
- **Assignee:** Correct person
- **Description:** Use template sections; be detailed

### Step 3: Link Dependencies
Link related backend, frontend, and integration issues.

### Step 4: Set MVP Sprint Day
Indicate which day (1–10) this should be completed.

---

## 🎯 Example Issue Workflow

### 1. Backend Creates API Contract
**Title:** `[API-SPEC] POST /api/v1/payments/initiate`
- Details: Request/response body, error codes, idempotency
- Status: Awaiting frontend approval

### 2. Frontend Reviews & Approves
- Approves in comment: "Contract looks good, starting frontend implementation"

### 3. Backend Implements Endpoint
**Title:** `[BE] Mobile Money Payment Initiation`
- Implements endpoint per contract
- Tests with real mobile money API
- Links to API contract issue

### 4. Frontend Integrates
**Title:** `[FE][Lead] Payment Flow UI`
- Builds payment form & confirmation screen
- Integrates with real `/api/v1/payments/initiate` endpoint
- Tests end-to-end

### 5. Integration Team Tests
**Title:** `[INT] Payment Initiation End-to-End`
- Tests full flow: user clicks Pay → sees confirmation → mobile money → success page
- Verifies wallet updates correctly
- Integration owner approves

### 6. QA Tests & Approves
**Title:** `[QA] Payment Flow Testing`
- Runs QA checklist (auth, payment, wallet update, etc.)
- Tests on mobile & desktop
- Signs off as ready for production

---

## 📞 Support & Questions

- **Project Lead:** Peter Zyambo
- **Backend:** George Mugale
- **Frontend:** George Mugale (Lead), Barnabas Mwaipaya (Support)
- **Integration Owner:** Peter Zyambo (or delegate)

---

## 🎯 Guiding Rule

> **If it doesn't help a creator get paid within 2 weeks, it does not ship.**

Keep all issues focused on this goal.
