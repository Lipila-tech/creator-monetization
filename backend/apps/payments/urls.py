from django.urls import path
from apps.payments.views.cashin import (
    AvailabilityAPIView,
    ActiveConfigAPIView,
    ResendCallbackAPIView,
    PaymentStatusAPIView,
    DepositAPIView,
    DepositCallbackAPIView,
)

app_name = "payments"

urlpatterns = [
    path("availability/", AvailabilityAPIView.as_view(), name="availability"),
    path("config/", ActiveConfigAPIView.as_view(), name="active_config"),
    path("deposits/<uuid:deposit_id>/resend-callback/", ResendCallbackAPIView.as_view(), name="resend_callback"),
    path("deposits/<uuid:deposit_id>/status/", PaymentStatusAPIView.as_view(), name="payment_status"),
    path("deposits/<slug:slug>/", DepositAPIView.as_view(), name="deposit"),
    path("deposits/callback/", DepositCallbackAPIView.as_view(), name="deposit_callback"),
]