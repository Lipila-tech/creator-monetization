# Backend API - TipZed Monetization MVP

Core service handling authentication, creator profiles, wallets, payments, payouts, and admin reconciliation.

---

## Overview
The backend API is built with Django REST Framework and provides endpoints for all core functionalities of the TipZed monetization platform. It handles user authentication, creator profile management, wallet operations, payment processing, payout requests, and admin reconciliation.

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
pip install -r requirements/dev.txt

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


## Environment Variables

Create `.env` file and copy required variables from `.env.example`.

---

## Authentication

Check the authentication documentation for details: [docs/AUTHENTICATION.md](docs/AUTHENTICATION.md)

### Roles
- `creator` - Can create profiles, receive payments, request payouts
- `patron` - Can view profiles, make donations and subscribe
- `admin` - Can view all data, approve payouts, reconcile transactions
- `guest` - Can view public profiles, make payments without account

---

## Live API Endpoints

**Base URL**: `https://lipila.schadmin.cloud/`

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

## Common Issues

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
**API Questions?** → Check documentation or ask in #backend channel
---

## Contributing Backend


**See [CONTRIBUTION.md](../CONTRIBUTION.md)**

**Contact:** Peter Zyambo (backend lead)

---

**Created:** January 27, 2026  
**Framework:** Django REST Framework  
**Database:** PostgreSQL  
**Status:** MVP Development
