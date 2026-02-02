from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from apps.wallets.models.payment_related import Wallet, WalletTransaction
from apps.wallets.services.payout_orchestrator import PayoutOrchestrator


def superuser_required(view_func):
    return user_passes_test(
        lambda u: u.is_active and u.is_superuser)(view_func)


@staff_member_required
@superuser_required
@require_http_methods(["GET", "POST"])
def finalise_wallet_payout(request, payout_tx_id):
    """
    Superuser-only view to finalise a pending wallet payout.
    GET  -> confirmation screen
    POST -> execute provider payout
    """

    payout_tx = get_object_or_404(
        WalletTransaction,
        id=payout_tx_id,
        transaction_type="PAYOUT",
        status="PENDING",
    )

    wallet = payout_tx.wallet
    app_label = wallet._meta.app_label
    model_name = wallet._meta.model_name

    wallet_change_url = reverse(
        f"lipila_admin:{app_label}_{model_name}_change",
        args=[wallet.id],
    )

    # =============================
    # STEP 1: Confirmation page
    # =============================
    if request.method == "GET":
        return render(
            request,
            "wallets/confirm_finalise_payout.html",
            {
                "wallet": wallet,
                "payout_tx": payout_tx,
                "wallet_change_url": wallet_change_url,
            },
        )

    # =============================
    # STEP 2: Finalise payout
    # =============================
    try:
        PayoutOrchestrator.finalize(
            payout_tx=payout_tx,
            success=True,
            approved_by=request.user,
        )

        messages.success(
            request,
            f"Payout finalised successfully "
            f"(Reference: {payout_tx.reference})",
        )

    except Exception as exc:
        messages.error(request, f"Payout finalisation failed: {exc}")

    return redirect(wallet_change_url)


@staff_member_required
@require_http_methods(["GET", "POST"])
def trigger_wallet_payout(request, wallet_id):
    """
    Staff-only view to manually trigger a wallet payout.
    GET  -> show confirmation screen
    POST -> initiate payout
    """

    wallet = get_object_or_404(Wallet, id=wallet_id)

    app_label = Wallet._meta.app_label
    model_name = Wallet._meta.model_name

    # Lipila admin wallet change page
    change_url = reverse(
        f"lipila_admin:{app_label}_{model_name}_change",
        args=[wallet.id],
    )

    # =============================
    # STEP 1: Confirmation page
    # =============================
    if request.method == "GET":
        return render(
            request,
            "wallets/confirm_payout.html",
            {
                "wallet": wallet,
                "change_url": change_url,
            },
        )

    # =============================
    # STEP 2: Execute payout
    # =============================
    try:
        payout_tx = PayoutOrchestrator.initiate_payout(
            wallet=wallet,
            initiated_by=request.user,
        )

        messages.success(
            request,
            f"Payout initiated successfully"
            f"(Reference: {payout_tx.reference})",
        )

    except Exception as exc:
        messages.error(request, f"Payout failed: {exc}")

    return redirect(change_url)
