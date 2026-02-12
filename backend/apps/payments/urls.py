from django.urls import path
from apps.payments.views import DepositAPIView
from apps.payments.webhooks import WebhookAPIView, PaymentStatusAPIView

app_name = "payments"

urlpatterns = [
    path("deposits/<uuid:wallet_id>/", DepositAPIView.as_view(), name="deposit"),
    path("webhook/", WebhookAPIView.as_view(), name="webhook"),
    path(
        "status/<uuid:payment_id>/",
        PaymentStatusAPIView.as_view(),
        name="payment_status",
    ),
]
