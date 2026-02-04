from django.urls import path
from apps.payments.views import  DepositAPIView

app_name = "payments"

urlpatterns = [
    path("deposits/<slug:slug>/", DepositAPIView.as_view(), name="deposit")
]