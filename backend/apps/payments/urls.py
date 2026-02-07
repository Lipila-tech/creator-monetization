from django.urls import path
from apps.payments.views import  DepositAPIView

app_name = "payments"

urlpatterns = [
    path("deposits/<uuid:wallet_id>/", DepositAPIView.as_view(), name="deposit")
]