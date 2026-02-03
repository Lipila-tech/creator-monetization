import json
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.payments.models import Payment
from apps.wallets.models import Invoice, WalletKYC
from utils.external_requests import pawapay_request


User = get_user_model()


def availability(request):
    data, code = pawapay_request(
        "GET", "/availability?country=ZMB&operationType=DEPOSIT"
    )
    return render(request, "payments/availability.html", {"data": data})


def active_config(request):
    data, code = pawapay_request(
        "GET", "/active-conf?country=ZMB&operationType=DEPOSIT"
    )
    return render(request, "payments/config.html", {"data": data})


def resend_callback(request, deposit_id):
    """Resends the deposit callback for a given deposit ID."""
    data, code = pawapay_request(
        "POST", f"/v2/deposits/resend-callback/{deposit_id}")
    return render(request, "payments/resend.html", {"data": data})


def payment_status(request, deposit_id):
    """
    Handles the payment status view for a given deposit ID.
    """
    payment = Payment.objects.filter(id=deposit_id).first()

    context = {
        "status": "Unknown", "message": "Unknown status", "statuses": []
    }
    if not payment:
        context = {
            "status": "failed",
            "message": "An error occurred. Please try again later.",
        }

    if payment.status == "rejected":
        failure_msg = payment.metadata["failureReason"]["failureMessage"]
        context["status"] = "rejected"
        context["message"] = failure_msg
        return render(request, "payments/status.html", context)
    data, code = pawapay_request("GET", f"/v2/deposits/{deposit_id}")
    if code == 200 and "data" in data:
        status = data["data"]["status"].lower()
        # Dont update status if pending/submitted to
        # avoid overwriting final state
        skip_statuses = [
            "pending",
            "submitted",
            "accepted",
            "processing",
            "in_reconciliation",
        ]
        if payment.status in skip_statuses and status in skip_statuses:
            status = payment.status
        payment.status = status
        payment.metadata = data["data"]
        payment.save()
        try:
            failure_msg = payment.metadata["failureReason"]["failureMessage"]
        except KeyError:
            failure_msg = "Unspecified Failure"

        if status in skip_statuses:
            message = "Approve transaction from PAWAPAY on your mobile device"
        elif status == "completed":
            message = "Transaction Completed"
        else:
            message = failure_msg
        context["status"] = status
        context["statuses"] = skip_statuses
        context["message"] = message
        
        return render(request, "payments/status.html", context)
    return render(request, "payments/status.html", context)


def deposit_invoice_payment(request, invoice_id=None):
    """Handles deposit payment for a given invoice."""

    invoice = get_object_or_404(Invoice, id=invoice_id)
    if request.method == "POST":
        amount = invoice.subtotal()
        phone = request.POST.get("phone")
        provider = request.POST.get("provider")
        isp_provider = request.POST.get("ispProvider")

        owner = (
            invoice.customer.owner
            if invoice.invoice_type == "CUSTOMER"
            else User.objects.filter(email=settings.ADMIN_USER_EMAIL).first()
        )

        if not hasattr(owner, "wallet"):
            return render(
                request,
                "payments/status.html",
                {
                    "status": "rejected",
                    "message": "User has no wallet to collect payment.",
                },
            )

        wallet = owner.wallet
        with transaction.atomic():
            payment = Payment.objects.create_payment(
                user=owner,
                amount=amount,
                customer_phone=f"260{phone}",
                provider=provider or "pawapay",
                isp_provider=isp_provider,
                wallet=wallet,
            )

        # SINGLE-PAYER LOGIC
        if not invoice.multiple_payers:
            if invoice.payment:
                return render(
                    request,
                    "payments/status.html",
                    {
                        "status": "rejected",
                        "message": "This invoice has already been paid.",
                    },
                )
            invoice.payment = payment
            invoice.save(update_fields=["payment"])

        # OPTIONAL: if you track payments via M2M or FK
        # InvoicePayment.objects.create(invoice=invoice, payment=payment)

        payload = {
            "amount": str(int(amount)),
            "currency": "ZMW",
            "depositId": str(payment.id),
            "payer": {
                "type": "MMO",
                "accountDetails": {
                    "provider": str(payment.isp_provider),
                    "phoneNumber": str(payment.customer_phone),
                },
            },
            "customerMessage": "Payment to SchaAdmin",
            "clientReferenceId": payment.reference,
            "metadata": [
                {
                    "paymentId": str(payment.id), "invoiceId": str(invoice.id)
                }
            ],
        }

        data, code = pawapay_request("POST", "/v2/deposits/", payload=payload)

        if code == 200:
            status = data.get("status", "").lower()
            payment.status = status
            payment.metadata = data
            payment.save()

            return redirect("lipila:payment_status", payment.id)

        return redirect("lipila:payment_status", payment.id)

    # ======================
    # GET REQUEST
    # ======================
    kyc = WalletKYC.objects.filter(wallet__user=invoice.customer.owner).first()
    payee = kyc.full_name if kyc else invoice.customer.owner.get_full_name()
    context = {
        "payee": payee,
        "amount": int(invoice.subtotal()),
        "remarks": invoice.remarks,
    }

    # ✅ Updated can_pay logic
    context["can_pay"] = invoice.status not in ["cancelled"] and (
        invoice.multiple_payers or not invoice.payment
    )

    return render(request, "payments/invoice_payment.html", context)
