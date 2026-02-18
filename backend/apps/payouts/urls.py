from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import finalise_wallet_payout, trigger_wallet_payout

app_name = "payouts"

urlpatterns = [
    path(
        "<uuid:wallet_id>/initiate/", trigger_wallet_payout, name="trigger_wallet_payout",
    ),
    path("<uuid:payout_tx_id>/finalise/", finalise_wallet_payout, name="finalise_wallet_payout",
         ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
