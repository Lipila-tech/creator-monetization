# 📋 Issue Template Documentation

This directory contains comprehensive issue templates and guides for the **Nthanda Monetization App MVP** (2-week sprint).

## 📚 Documentation Files

### 1. [ISSUE_TEMPLATE_GUIDE.md](ISSUE_TEMPLATE_GUIDE.md) 📖
**Complete reference guide with:**
- Overview of all 9 issue templates
- When to use each template
- 2-week sprint timeline
- Daily milestones for backend & frontend
- Integration windows & handshake checklist
- Definition of done (MVP)
- Labeling conventions
- Team roles & responsibilities

**👉 Start here** if you're new to the project.

---

### 2. [ISSUE_TEMPLATES_QUICK_REF.md](ISSUE_TEMPLATES_QUICK_REF.md) ⚡
**Quick one-page reference card:**
- Template comparison table
- Sprint structure overview
- MVP definition of done
- Core API endpoints
- Key labels
- Team roles matrix
- Common issue titles
- Typical workflow

**👉 Keep this handy** during sprint planning.

---

### 3. [EXAMPLE_WEEK1_ISSUES.md](EXAMPLE_WEEK1_ISSUES.md) 📝
**Real example issues for Week 1:**
- 19 detailed example issues (Days 1-10)
- Auth, profiles, wallet, payments, payouts, admin flows
- Shows proper structure, acceptance criteria, dependencies
- Links issues together showing realistic workflow

**👉 Use as templates** when creating actual issues.

---

## 🗂️ Issue Templates (.github/ISSUE_TEMPLATE/)

| File | Template | Use Case |
|------|----------|----------|
| `backend-feature.md` | `[BE]` | API endpoints, models, services |
| `frontend-lead.md` | `[FE][Lead]` | Core UI features, pages |
| `frontend-support.md` | `[FE][Support]` | UI polish, styling, accessibility |
| `integration.md` | `[INT]` | Backend–Frontend integration |
| `api-contract.md` | `[API-SPEC]` | API specification & contracts |
| `qa-go-live.md` | `[QA]` | Testing, verification, launch |
| `devops.md` | `[DevOps]` | Deployment, infrastructure, monitoring |
| `config.md` | `[CONFIG]` | Environment setup, secrets |
| `bug-report.md` | `[BUG]` | Defect reports |

---

## 🚀 Quick Start

### For Project Leads
1. Read [ISSUE_TEMPLATE_GUIDE.md](ISSUE_TEMPLATE_GUIDE.md)
2. Review [EXAMPLE_WEEK1_ISSUES.md](EXAMPLE_WEEK1_ISSUES.md)
3. Create first batch of issues using those examples
4. Assign to team members

### For Developers
1. Read [ISSUE_TEMPLATES_QUICK_REF.md](ISSUE_TEMPLATES_QUICK_REF.md)
2. When you get an issue, check the template type
3. Ensure you understand acceptance criteria
4. Link to related issues
5. Daily sync with other team members

### For Integration Owner
1. Review [ISSUE_TEMPLATE_GUIDE.md](ISSUE_TEMPLATE_GUIDE.md) section on "Daily Backend–Frontend Handshake"
2. Use `[API-SPEC]` template to define contracts before implementation
3. Verify integrations using `[INT]` template checklist
4. Sign-off on merged PRs matching API contracts

### For QA Team
1. Use `[QA]` template for testing issues
2. Follow MVP QA Checklist
3. Verify all acceptance criteria met
4. Test on mobile + desktop
5. Sign-off before deployment

---

## 📊 2-Week Sprint Overview

```
┌─────────────────────────────────────────────────────┐
│ WEEK 1: Foundation & Integrations                   │
├─────────────────────────────────────────────────────┤
│ Day 1-2:  Auth setup, user models, login/signup     │
│ Day 3-5:  First integrations, creator profiles      │
│ Day 6-7:  Payment flow, webhooks, end-to-end test   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ WEEK 2: Features, Polish & Launch                   │
├─────────────────────────────────────────────────────┤
│ Day 8:    UI polish, admin features                 │
│ Day 9:    Bug fixes, integration issues             │
│ Day 10:   Security review, production deployment    │
└─────────────────────────────────────────────────────┘
```

### Integration Windows
- **Days 3–5:** First live backend–frontend integrations
- **Days 6–7:** Full payment & payout end-to-end flows  
- **Days 9–10:** Stabilization, regression testing, go-live

---

## ✅ MVP Definition of Done

A feature is **Done** when:

1. **✅ Code Quality**
   - Meets acceptance criteria
   - Unit/integration tests written
   - No console errors/warnings
   - Code reviewed & approved

2. **✅ Integration**
   - API contract defined & approved
   - Real backend endpoint used (no mocks)
   - End-to-end flow tested
   - Integration owner sign-off

3. **✅ Testing**
   - QA verified on mobile & desktop
   - All browsers tested
   - No regressions
   - Smoke tests pass

4. **✅ Documentation**
   - API contract documented
   - Deployment instructions clear
   - Known limitations noted

---

## 🎯 Core Principles

### 1. API Contracts First ✅
- Create `[API-SPEC]` **before** implementing
- Backend & frontend must agree
- Document request/response/errors

### 2. Real Backend Integration ✅
- Frontend uses **real** backend endpoints
- No mock data in production
- Integration tested daily

### 3. Daily Backend–Frontend Sync ✅
- Days 3–10: Teams check in daily
- Verify API contracts
- Block merges that break APIs
- Log issues same day

### 4. Integration Owner Approval ✅
- All API changes need sign-off
- Must verify contract is met
- Can block PRs if API broken

### 5. MVP Focus ✅
- **"If it doesn't help a creator get paid in 2 weeks, don't ship it"**
- Cut scope, not quality
- Prioritize core payment flow

---

## 🔗 Core API Endpoints (MVP)

**Authentication:**
```
POST   /api/v1/auth/register         Create user
POST   /api/v1/auth/login            User login
POST   /api/v1/auth/refresh          Refresh token
```

**Creator Profiles:**
```
GET    /api/v1/creators/{id}         Get creator profile
PUT    /api/v1/creators/me           Update own profile
```

**Wallet & Payments:**
```
GET    /api/v1/wallets/me            Get wallet & balance
GET    /api/v1/wallets/me/transactions  Transaction history
POST   /api/v1/payments/initiate     Initiate payment
POST   /api/v1/payments/webhook      Payment webhook (from provider)
```

**Payouts:**
```
POST   /api/v1/payouts/request       Request payout
GET    /api/v1/payouts/me            Get own payout history
```

**Admin:**
```
GET    /api/v1/admin/transactions    View all transactions
GET    /api/v1/admin/payouts         View all payouts
POST   /api/v1/admin/payouts/{id}/approve    Approve payout
POST   /api/v1/admin/payouts/{id}/reject     Reject payout
```

---

## 👥 Team Roles

| Role | Person | Responsibilities |
|------|--------|-----------------|
| **Project Lead** | Peter Zyambo | Overall MVP delivery, integration owner |
| **Backend** | George Mugale | All API endpoints & services |
| **Frontend Lead** | George Mugale | Core UI features & state mgmt |
| **Frontend Support** | Barnabas | Styling, responsiveness, polish |
| **QA** | Team | Testing & launch readiness |

---

## 🏷️ Label Conventions

**Every issue should have:**

**Type:**
- `backend` — Backend feature/service
- `frontend` — Frontend feature/UI
- `integration` — Backend–Frontend integration
- `qa` — Testing & QA
- `devops` — Deployment & infrastructure
- `bug` — Defect report

**Priority:**
- `high-priority` — Blocks other work or MVP launch
- (Not required if low priority)

**Sprint:**
- `2-week-mvp` — Required for MVP launch
- (Issues without this tag are post-launch)

**Ownership:**
- `frontend-lead` — George's responsibility
- `frontend-support` — Barnabas's responsibility

---

## 📝 Creating Your First Issue

1. **Choose template** based on work type (backend, frontend, integration, etc.)
2. **Fill in title:** Clear & specific (e.g., `[BE] Auth & JWT Models`)
3. **Add labels:** Type + priority + `2-week-mvp`
4. **Assign owner:** Person responsible
5. **Link dependencies:** Other related issues
6. **Set day:** Which sprint day (1–10)
7. **Fill description:** Use template sections

---

## 🔗 Useful Links

- [GitHub Issues](https://github.com/zyambo/creator-monetization/issues)
- [Project Board](https://github.com/zyambo/creator-monetization/projects)
- [Pull Requests](https://github.com/zyambo/creator-monetization/pulls)

---

## ❓ FAQ

**Q: Which template should I use?**
A: See [ISSUE_TEMPLATES_QUICK_REF.md](ISSUE_TEMPLATES_QUICK_REF.md) table.

**Q: How do I define an API endpoint?**
A: Use `[API-SPEC]` template with full request/response examples.

**Q: When should frontend start coding?**
A: After API contract (`[API-SPEC]`) is approved.

**Q: What if a feature is blocked?**
A: Create issue with `[blocked-by: #XXX]` in title or label.

**Q: How often should teams sync?**
A: Daily during integration windows (Days 3–10).

**Q: What's the minimum acceptable test coverage?**
A: 80% for backend services, manual + automated for frontend.

---

## 🎓 Training & Onboarding

1. **New team member joins?**
   - Have them read [ISSUE_TEMPLATE_GUIDE.md](ISSUE_TEMPLATE_GUIDE.md)
   - Show them [EXAMPLE_WEEK1_ISSUES.md](EXAMPLE_WEEK1_ISSUES.md)
   - Pair with senior dev for first issue

2. **Need quick refresher?**
   - Check [ISSUE_TEMPLATES_QUICK_REF.md](ISSUE_TEMPLATES_QUICK_REF.md)

3. **Want to see real examples?**
   - Look at [EXAMPLE_WEEK1_ISSUES.md](EXAMPLE_WEEK1_ISSUES.md)

---

## 🚀 Good Luck! 

**Remember:** Our mission is to help creators in Zambia get paid reliably.

Every issue should move us closer to that goal. If it doesn't help creators get paid within 2 weeks, **don't ship it**.

Let's build something meaningful! 🇿🇲
