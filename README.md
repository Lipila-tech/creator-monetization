# 🇿🇲 TipZed Monetization App - MVP

## Overview

This repository contains the code and documentation for the TipZed Monetization MVP, focused on enabling Zambian creators to get paid locally. The backend API is built with Django REST Framework and provides endpoints for authentication, creator profiles, wallets, payments, payouts, and admin reconciliation. The frontend is built with React and integrates with the backend to provide a seamless user experience.

---

## MVP Scope

**Core User Flows:**
- [x] Creators sign up, create profiles, set up payout accounts (mobile money or bank)
- [x] Fans discover creators, send payments via mobile money
- [x] Creators see balances, request payouts
- [x] Admin approves payouts, reconciles transactions


## Quick Start

Read the backend readme for API setup and development instructions: [backend/README.md](backend/README.md)

### Setup Frontend

Read the frontend readme for UI setup and development instructions: [frontend/README.md](frontend/README.md)

---

## System Architecture

![System Architecture Diagram](docs/system-architecture.png)

##  Complete Payment Flow

![Payment Flow Diagram](docs/payment-flow.png)

## Core Components

### Auth & User Service
- User registration (email + password) and social login (Google OAuth)
- JWT authentication with access and refresh tokens
- Role-based access control (creator, patron, admin, guest)
- JWT authentication & refresh tokens

### Creator Profiles Service
- Public creator profiles (discoverable)
- Profile editing
- Dashboard for creators to view stats, manage payouts

### Wallet & Ledger Service
- Immutable transaction ledger (append-only)
- Wallet balance calculated from ledger
- No manual balance editing (audit trail)
- Receive weekly payouts from TIPZED
- Idempotent payment processing (prevent duplicates)

### Payments Integration
- Initiate mobile money payments
- Webhook handling from mobile money provider
- Payment state machine (pending → success/failed)
- Idempotency (prevent duplicate charges)

### Payouts & Admin
- Creator payout requests
- Admin approval/rejection
- Automatic weekly payout processing
- Admin reconciliation dashboard

---

## 📖 Documentation

### Getting Started
- **[backend/README.md](backend/README.md)** - Backend setup & development
- **[frontend/README.md](frontend/README.md)** - Frontend setup & development

### API Reference
- Swagger UI: `http://localhost:8000/api/docs/`
- Redocs UI: `http://localhost:8000/api/redocs/`
- Postman Collection: [postman_collection.json](docs/postman_collection.json)

---

## Team

| Role | Name | Responsibility |
|------|------|-----------------|
| **Project Lead** | Peter Zyambo | Overall MVP delivery, Backend lead, integration owner |
| **Frontend Lead** | George Mugale | Core UI, state management |
| **Frontend Support** | Barnabas Mwaipaya | Styling, responsiveness, polish |
| **Backend Support, QA** | Sepiso23 | services, database, polish |
| **QA** | Team | Testing, verification |

---


**Having trouble?**
- Backend issues → Contact Peter
- Frontend issues → Contact George or Barnabas
- Integration issues → Contact Peter

---

## License

MIT License - See LICENSE file

---

## Mission Statement

> **"If it doesn't help a creator get paid, don't ship it."**

Every decision, every line of code, every feature should move us toward this goal. Keep this focus and we will succeed.

---

## Contributing

Want to contribute? Start here:

- **Read [CONTRIBUTION.md](docs/CONTRIBUTION.md)** for:

- **Create issues** using templates in [.github/ISSUE_TEMPLATE](https://github.com/zyambo/creator-monetization/tree/main/.github/ISSUE_TEMPLATE/)

---

**Created:** January 27, 2026  
**Status:** MVP In Development  
**Timeline:** 2-week sprint  
**Goal:** Enable Zambian creators to get paid reliably.
