Build & test commands

- Run dev server: python manage.py runserver
- Install deps: pip install -r requirements/development.txt
- Run full tests: pytest
- Run a single test file: pytest tests/test_utils/test_external_requests.py
- Run a single test case: pytest tests/test_utils/test_external_requests.py::TestPawapayRequest::test_success_json_response
- Lint: flake8 .

High-level architecture

- Django REST Framework backend split into apps: customauth, creators, payments, payouts, wallets, customadmin.
- Celery workers for background tasks; Redis used for cache/broker. Settings live under config/settings/*.py.
- Payments app integrates external mobile-money gateways; webhooks update Payment and Wallet services.

Key conventions

- Tests use pytest with DJANGO_SETTINGS_MODULE=config.settings.test (see pytest.ini).
- External gateway helpers live in utils/external_requests.py; keep pawapay_request for legacy but add gateway-specific helpers when needed.
- Webhooks: apps/payments/webhooks.py writes PaymentWebhookLog and updates Payment.external_id/provider_data. Include raw_payload when creating logs.
- Env vars: copy .env.dist -> .env; secrets are loaded via django-environ in config settings.
- Use Payment.generate_reference() for external references; avoid changing reference format without a migration.

Incorporated docs

- README.md: setup, runserver, testing instructions

If you'd like, I can also add CI workflow snippets or configure an MCP server for Playwright or other tooling. Let me know.