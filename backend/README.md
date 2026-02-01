# Backend API - TipZed Monetization MVP

**Django REST Framework API for creator monetization platform**

Core service handling authentication, creator profiles, wallets, payments, payouts, and admin reconciliation.

---

## Overview

RESTful API serving the TipZed web app. Handles:
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

## Project Structure

```
backend/
├── config/                  ← Django project settings
├── apps/                    ← Django apps
├── tests/                   ← Test cases
├── utils/                   ← Utility functions and helpers
├── middleware/
├── manage.py                ← Django CLI
├── requirements.txt         ← Python dependencies
├── .env.example             ← Environment variables template
├── pytest.ini               ← Pytest configuration
└── README.md                ← This file
```

---

## Setup

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

Create `.env` file and copy required variables from `.env.example`.

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

## Live API Endpoints

**Base URL**: `https://tipzed.pythonanywhere.com/`

**Check the documentation for API endpoints at:**
- swagger: https://tipzed.pythonanywhere.com/api/v1/schema/swagger-ui/
- redoc: https://tipzed.pythonanywhere.com/api/v1/schema/docs/

**Or Test in Postman Collection:**
- [Postman Collection Link]('#')
---


## Testing

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
pytest.ini is preconfigured for coverage reports. update `pytest.ini` if needed.

---

## Monitoring & Logging

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


## Development Guidelines

### Creating New Endpoint

1. Define `models.py` (database schema)
2. Create `serializers.py` (validation)
3. Build `views.py` (logic)
4. Add `urls.py` routing
5. Write tests in `tests` folder
6. Create migration: `python manage.py makemigrations`


### Testing New Feature

1. Write test before code (TDD)
2. Implement feature
3. Run tests: `pytest`
4. Verify with API client (Postman)

### Code Style
- Follow PEP 8
- Use black for formatting
- Use flake8 for linting
- Type hints for functions
- Docstrings on classes/functions

---

## Deployment

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

## Support

**Backend Issues?** → Contact Peter Zyambo

**Need Help?**
- Check [technical architecture](../README.md)
- Review [ISSUE_TEMPLATE_GUIDE.md](../ISSUE_TEMPLATE_GUIDE.md)
- See [EXAMPLE_WEEK1_ISSUES.md](../EXAMPLE_WEEK1_ISSUES.md) for patterns

---

## Contributing Backend

Want to help with backend development?

**See [CONTRIBUTION.md](../CONTRIBUTION.md)**

**Contact:** Peter Zyambo (backend lead)

---

**Created:** January 27, 2026  
**Framework:** Django REST Framework  
**Database:** PostgreSQL  
**Status:** MVP Development
