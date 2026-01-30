# Backend API - Tip Zed Monetization MVP

**Django REST Framework API for creator monetization platform**

Core service handling authentication, creator profiles, wallets, payments, payouts, and admin reconciliation.

---

## 🎯 Overview

RESTful API serving the Tip Zed web app. Handles:
- User authentication (JWT)
- Creator profiles & public endpoints
- Immutable wallet ledger
- Payment processing & webhooks
- Payout management & admin approval
- Transaction reconciliation

**Tech Stack:**
- Django 4.2
- Django REST Framework
- PostgreSQL (ledger)
- Redis (caching/queues)
- Celery (async tasks)
- pytest (testing)

---

## 📁 Project Structure

```
backend/
├── config/
│   ├── settings.py          ← Django settings (ENV-based)
│   ├── urls.py              ← Main URL config
│   ├── wsgi.py              ← WSGI entry point
│   └── celery.py            ← Celery configuration
├── apps/
│   ├── customauth/
│   │   ├── migrations/      ← Database migrations
│   │   ├── models.py        ← User model with roles
│   │   ├── views.py         ← Auth endpoints (register, login, refresh)
│   │   ├── serializers.py   ← Request/response validation
│   │   ├── permissions.py   ← Role-based permissions
│   │   └── urls.py          ← Auth routes
│   ├── creators/
│   │   ├── migrations/      ← Database migrations
│   │   ├── models.py        ← Creator profile model
│   │   ├── views.py         ← Profile endpoints
│   │   ├── serializers.py   ← Profile serialization
│   │   └── urls.py
│   ├── wallets/
│   │   ├── migrations/      ← Database migrations
│   │   ├── models.py        ← Wallet & transaction ledger
│   │   ├── views.py         ← Wallet endpoints
│   │   ├── serializers.py
│   │   ├── services.py      ← Business logic
│   │   └── urls.py
│   ├── payments/
│   │   ├── migrations/      ← Database migrations
│   │   ├── models.py        ← Payment model
│   │   ├── views.py         ← Payment endpoints
│   │   ├── webhooks.py      ← Mobile money webhooks
│   │   ├── services.py      ← Payment processing
│   │   └── urls.py
│   ├── payouts/
│   │   ├── migrations/      ← Database migrations
│   │   ├── models.py        ← Payout request model
│   │   ├── views.py         ← Payout endpoints
│   │   ├── services.py      ← Payout processing
│   │   └── urls.py
│   └── customadmin/
│       ├── views.py         ← Admin endpoints
│       ├── serializers.py
│       ├── permissions.py   ← Admin-only access
│       └── urls.py
├── tests/
|── conftest.py              ← Pytest fixtures
|── factories.py             ← Test data factories
├── utils/
├── middleware/
├── management/
│   └── commands/            ← Custom management commands
├── manage.py                ← Django CLI
├── requirements.txt         ← Python dependencies
├── .env.example             ← Environment variables template
├── pytest.ini               ← Pytest configuration
└── README.md                ← This file
```

---

## 🚀 Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+

### Installation

```bash
# Clone repo
git clone https://github.com/zyambo/creator-monetization.git
cd creator-monetization/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Database setup
python manage.py migrate
python manage.py createsuperuser  # Create admin user

# Run development server
python manage.py runserver
```

→ API available at `http://localhost:8000`

---

## 📝 Environment Variables

Create `.env` file:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/Tip Zed_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your-jwt-secret
JWT_EXPIRY=3600
JWT_REFRESH_EXPIRY=604800

# Mobile Money Provider
MOBILE_MONEY_API_KEY=your-api-key
MOBILE_MONEY_API_URL=https://api.provider.com
MOBILE_MONEY_WEBHOOK_SECRET=webhook-secret

# Email (for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password

# Sentry (error tracking)
SENTRY_DSN=

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

## 🔐 Authentication

### JWT Flow

1. **Register / Login** → Returns `access_token` + `refresh_token`
2. **API Request** → Send `Authorization: Bearer <access_token>`
3. **Token Expires** → Use `refresh_token` to get new `access_token`

### Roles
- `creator` - Can create profiles, receive payments, request payouts
- `fan` - Can view profiles, send payments
- `admin` - Can view all data, approve payouts, reconcile transactions

---

## 📡 API Endpoints

### Authentication
All Auth Endpoints:

Headers: `X-API-KEY: <client_api_key>`

```
POST /api/v1/auth/register/
Body: { email, password1,password2, first_name, last_name, user_type }
Returns: { access_token, refresh_token, user }

POST /api/v1/auth/login/
Body: { email, password }
Returns: { access_token, refresh_token, user }

POST /api/v1/auth/refresh/
Body: { refresh_token }
Returns: { access_token }

GET /api/v1/auth/profile/
Returns: Own creator profile + bank account

PATCH /api/v1/profile/
body: { first_name, last_name, password }
Returns: Updated user info


PUT /api/v1/profile/
Body: { 
   bio, bank_account, first_name, last_name, profile_image, cover_image
 }
Returns: Updated profile
```

### Creator Profiles (Public)

```

GET /api/v1/creators/all
Auth: Not required (public)
Returns: {
   "status": "success",
   "data": [ list of creator profiles ]
 } 

GET /api/v1/creators/{slug}
Auth: Not required (public)
Returns: { 
   "status": "success",
   "data": { creator profile fields }
 }
```

### Wallet & Transactions

```
GET /api/v1/wallets/me
Auth: Required (creator)
Returns: { balance, currency, transactions[] }

GET /api/v1/wallets/me/transactions?limit=20&offset=0
Auth: Required (creator)
Returns: Paginated transaction history
```

### Payments

```
POST /api/v1/payments/initiate
Auth: Required (fan)
Body: { creator_id, amount, currency, message }
Headers: X-Idempotency-Key: <uuid>
Returns: { payment_id, status, mobile_money_url }

POST /api/v1/payments/webhook
Auth: Not required (mobile money provider)
Body: { payment_id, status, timestamp }
Returns: { status: success }
```

### Payouts

```
POST /api/v1/payouts/request
Auth: Required (creator)
Body: { amount, bank_account, account_name }
Returns: { payout_id, status, amount }

GET /api/v1/payouts/me
Auth: Required (creator)
Returns: Payout request history
```

### Admin

```
GET /api/v1/admin/transactions?status=success&limit=50
Auth: Required (admin)
Returns: All transactions

GET /api/v1/admin/payouts
Auth: Required (admin)
Returns: All payout requests

POST /api/v1/admin/payouts/{id}/approve
Auth: Required (admin)
Body: { note }
Returns: Updated payout with approved status

POST /api/v1/admin/payouts/{id}/reject
Auth: Required (admin)
Body: { reason }
Returns: Updated payout with rejected status
```

---

## 📋 Database Schema

### User
```sql
id (UUID)
email (unique)
password (hashed)
full_name
role (creator | fan | admin)
created_at
updated_at
```

### Creator Profile
```sql
id (UUID)
user_id (FK)
bio
avatar_url
bank_account
account_name
followers_count
created_at
updated_at
```

### Wallet
```sql
id (UUID)
creator_id (FK)
balance (calculated from ledger)
currency (ZMW)
created_at
updated_at
```

### Transaction Ledger
```sql
id (UUID)
wallet_id (FK)
amount
type (payment | payout | refund)
status (pending | success | failed)
payment_id (FK, nullable)
payout_id (FK, nullable)
created_at
```

### Payment
```sql
id (UUID)
fan_id (FK)
creator_id (FK)
amount
currency
status (pending | success | failed)
provider_transaction_id
message
created_at
updated_at
```

### Payout
```sql
id (UUID)
creator_id (FK)
amount
status (pending | approved | rejected | completed)
bank_account
account_name
admin_id (FK, nullable)
admin_note
created_at
updated_at
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific App Tests
```bash
pytest apps/auth/tests.py
pytest apps/payments/tests.py
```

### Run with Coverage
```bash
pytest --cov=apps --cov-report=html
```

---

## 🔄 Payment Flow

1. **Initiate Payment**
   - Fan calls `POST /payments/initiate`
   - System creates payment record (status: pending)
   - Returns mobile money URL

2. **Mobile Money Processing**
   - Fan redirected to mobile money provider
   - User confirms payment on phone
   - Provider processes payment

3. **Webhook Callback**
   - Provider sends webhook with payment status
   - System verifies webhook signature
   - Updates payment status (success/failed)
   - If success: creates transaction ledger entry, updates wallet

4. **Idempotency**
   - Duplicate webhooks are idempotent
   - Payment only credited once
   - Uses idempotency key to prevent duplicates

---


## 📊 Monitoring & Logging

### Logs
- All endpoints log requests/responses
- Error stack traces captured
- Payment/payout operations logged
- User actions auditable

### Monitoring
- Sentry for error tracking
- DataDog/New Relic for performance
- Database slow query logs
- Redis memory monitoring

---

## 🐛 Common Issues

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -U postgres -h localhost
```

### Redis Connection Error
```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```


## 📚 Development Guidelines

### Creating New Endpoint

1. Define `models.py` (database schema)
2. Create `serializers.py` (validation)
3. Build `views.py` (logic)
4. Add `urls.py` routing
5. Write tests in `tests.py`
6. Create migration: `python manage.py makemigrations`
7. Document in API docs

### Testing New Feature

1. Write test before code (TDD)
2. Implement feature
3. Run tests: `pytest`
4. Check coverage: `pytest --cov`
5. Verify with API client (Postman)

### Code Style
- Follow PEP 8
- Use black for formatting
- Use flake8 for linting
- Type hints for functions
- Docstrings on classes/functions

---

## 🚀 Deployment

### Staging
```bash
git push origin feature-branch
# Auto-deploys to staging
```

### Production
```bash
git push origin main
# Auto-deploys to production
```

### Manual Deployment
```bash
# On server
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
sudo systemctl restart gunicorn
```

---

## 📞 Support

**Backend Issues?** → Contact Peter Zyambo

**Need Help?**
- Check [technical architecture](../README.md)
- Review [ISSUE_TEMPLATE_GUIDE.md](../ISSUE_TEMPLATE_GUIDE.md)
- See [EXAMPLE_WEEK1_ISSUES.md](../EXAMPLE_WEEK1_ISSUES.md) for patterns

---

## 🤝 Contributing Backend

Want to help with backend development?

**See [CONTRIBUTION.md](../CONTRIBUTION.md)**

**Contact:** Peter Zyambo (backend lead)

---

**Created:** January 27, 2026  
**Framework:** Django REST Framework  
**Database:** PostgreSQL  
**Status:** MVP Development
