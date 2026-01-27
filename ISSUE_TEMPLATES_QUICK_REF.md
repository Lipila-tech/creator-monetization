# 🚀 Nthanda MVP - Issue Template Quick Reference

## When to Use Each Template

| Template | Use When | Owner | Label |
|----------|----------|-------|-------|
| **[BE] Backend Feature** | Building API endpoints, models, services | Backend Dev | `backend` |
| **[FE][Lead] Frontend** | Core UI features, pages, state mgmt | George | `frontend-lead` |
| **[FE][Support] UI Polish** | Styling, responsiveness, accessibility | Barnabas | `frontend-support` |
| **[INT] Integration** | Testing backend + frontend together | Integration Owner | `integration` |
| **[API-SPEC] API Contract** | Defining endpoint specs before coding | Integration Owner | `api-contract` |
| **[QA] Testing & Go-Live** | Testing, verification, launch checklist | QA Team | `qa` |
| **[DevOps] Deployment** | Env setup, CI/CD, monitoring, backups | DevOps | `devops` |
| **[CONFIG] Configuration** | Environment vars, secrets, setup | Team Lead | `config` |
| **[BUG] Bug Report** | Reporting defects | Anyone | `bug` |

---

## 📅 2-Week Sprint Structure

```
Week 1:
  Day 1-2:  Backend auth + frontend setup
  Day 3-5:  First integrations + features
  Day 6-7:  Payment & payout flows
  
Week 2:
  Day 8:    Polish & final features
  Day 9:    Bug fixes & integration issues
  Day 10:   Security review + go-live
```

---

## ✅ MVP Definition of Done

Feature is **Done** when:
1. ✅ Code meets acceptance criteria
2. ✅ Tested (unit tests for backend, manual + automated for frontend)
3. ✅ Integrated with real API (no mocks)
4. ✅ QA verified on mobile & desktop
5. ✅ No console errors or warnings
6. ✅ Integration owner approved

---

## 🔗 Core API Endpoints

```
POST   /api/v1/auth/register         → Create user
POST   /api/v1/auth/login            → User login
GET    /api/v1/creators/{id}         → Get creator profile
GET    /api/v1/wallets/me            → Creator's wallet
POST   /api/v1/payments/initiate     → Start payment
GET    /api/v1/wallets/me/transactions → Transaction history
POST   /api/v1/payouts/request       → Request payout
GET    /api/v1/admin/transactions    → Admin: all transactions
POST   /api/v1/admin/payouts/{id}/approve → Approve payout
```

---

## 🎯 Key Labels

Always use:
- `2-week-mvp` — This is required for launch
- Type: `backend` | `frontend` | `integration` | `qa` | `devops` | `bug`
- Priority: `high-priority` (if blocking other work)

---

## 📊 Team Roles

| Role | Person | Responsibility |
|------|--------|-----------------|
| Project Lead | Peter Zyambo | Overall MVP delivery, integration owner |
| Backend Dev | George Mugale | All API endpoints & services |
| Frontend Lead | George Mugale | Core UI features & state management |
| Frontend Support | Barnabas | Styling, responsiveness, polish |
| QA | Team | Testing & launch readiness |

---

## 🚨 Critical Rules

1. **No Mocks in Production** — Frontend uses REAL backend endpoints
2. **API Contracts First** — Create `[API-SPEC]` before implementing
3. **Daily Handshake** — Backend + frontend sync daily (Days 3-10)
4. **Integration Owner Approval** — All API changes need sign-off
5. **Test Everything** — Mobile + desktop, all error cases

---

## 💡 Common Issue Titles

**Backend:**
- `[BE] Authentication & JWT Setup`
- `[BE] Creator Wallet Model`
- `[BE] Mobile Money Payment Endpoint`
- `[BE] Admin Payout Approval`

**Frontend:**
- `[FE][Lead] Login & Signup Forms`
- `[FE][Lead] Creator Dashboard`
- `[FE][Lead] Payment Confirmation UI`
- `[FE][Support] Mobile Responsiveness`

**Integration:**
- `[INT] Auth Flow Testing`
- `[INT] Payment Flow End-to-End`
- `[INT] Wallet Sync Verification`

**QA:**
- `[QA] Auth Flows Testing`
- `[QA] Payment Processing Testing`
- `[QA] Production Go-Live Checklist`

---

## 🔄 Typical Issue Workflow

1. **Create `[API-SPEC]`** → Define endpoint contract
2. **Approve Contract** → Backend + frontend agree
3. **Create `[BE]`** → Backend implements endpoint
4. **Create `[FE][Lead]`** → Frontend builds UI
5. **Create `[INT]`** → Test together end-to-end
6. **Create `[QA]`** → QA verifies & tests
7. **Merge** → Feature ready for production

---

**Guiding Rule:** If it doesn't help a creator get paid in 2 weeks, don't ship it.
