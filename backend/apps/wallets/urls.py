from django.urls import path
from apps.wallets.views import (
    WalletListView, WalletTransactionsView, WalletKYCView)

app_name = 'wallets'

urlpatterns = [
    path('me/', WalletListView.as_view(), name='user_wallet'),
    path('kyc/', WalletKYCView.as_view(), name='wallet_kyc'),
    path('transactions/', WalletTransactionsView.as_view(), name='wallet_transactions'),
]