from apps.wallets.services.transaction_service import WalletTransactionService


class PayoutService:

    @staticmethod
    def initiate_payout(*, wallet, amount, provider_client):
        """
        Initiate a payout from the wallet to the provider.
        Args:
            wallet (Wallet): The wallet to payout from.
            amount (Decimal): The amount to payout.
            provider_client (ProviderClient): The payment provider client.
        Returns:
            WalletTransaction: The created payout transaction.
        """
        reference = provider_client.generate_reference()

        tx = WalletTransactionService.payout(
            wallet=wallet,
            amount=amount,
            reference=reference,
        )

        provider_client.send_payout(
            amount=amount,
            phone_number=wallet.payout_account.phone_number,
            reference=reference,
        )

        return tx
