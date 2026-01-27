---
name: QA / Go-Live Checklist
about: Testing and launch readiness for MVP
title: "[QA] "
labels: ["qa", "go-live", "2-week-mvp"]
---

## 🔍 Test Area
What feature or flow is being tested?
Example: Authentication Flow, Payment Processing, Payout Approval, Admin Dashboard

## ✅ MVP QA Checklist
All auth flows tested:
- [ ] Login successful with valid credentials
- [ ] Login fails gracefully with invalid credentials
- [ ] JWT token expires and refresh works
- [ ] Logout clears session

Payment flow tested:
- [ ] Mobile money payments succeed
- [ ] Payment failures handled gracefully
- [ ] Duplicate payment callbacks are idempotent
- [ ] Wallet balance updates correctly after payment

Wallet & Ledger:
- [ ] Wallet balance matches ledger sum
- [ ] Transaction history displays correctly
- [ ] No manual balance edits possible

Payouts:
- [ ] Payout requests can be created
- [ ] Admin can approve/reject payouts
- [ ] Wallet balance updates after payout
- [ ] Payout account validation works

Admin & Reconciliation:
- [ ] Admin can view all transactions
- [ ] Filtering by status/date works
- [ ] All data is consistent

Error handling:
- [ ] UI displays user-friendly error messages
- [ ] No console errors or warnings
- [ ] Network errors handled gracefully

## 🌐 Browser & Device Testing
- [ ] Chrome (latest) - Desktop
- [ ] Firefox (latest) - Desktop
- [ ] Safari - macOS
- [ ] Safari Mobile - iOS (iPhone 6+)
- [ ] Chrome Mobile - Android

## 🚨 Issues Found
List bugs or concerns:
- Issue #XXX: [description]
- Issue #YYY: [description]

## 🚀 Go-Live Status
- [ ] **Ready for Production**
- [ ] Needs Fixes (block deploy)
- [ ] Blocked by: (link issues)

## 📋 Production Readiness Checklist
- [ ] All critical bugs fixed
- [ ] Performance acceptable (Lighthouse > 80)
- [ ] Monitoring and logging enabled
- [ ] Backup plan confirmed
- [ ] Support contact ready
- [ ] Database backups in place

