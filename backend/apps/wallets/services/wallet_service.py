from django.db.models import Sum, Q
from utils.exceptions import WalletNotFound, WalletError


class WalletService:
    """Core wallet operations."""

    @staticmethod
    def get_wallet_for_user(user):
        """Fetches the wallet for a given user.
        Args:
            user (User): The user instance.
        Returns:
            Wallet: The wallet instance associated with the user.
        Raises:
            WalletNotFound: If the user does not have a wallet.
        """
        try:
            return user.creator_profile.wallet
        except Exception:
            raise WalletNotFound("User does not have a wallet")

    @staticmethod
    def recalculate_wallet_balance(wallet):
        """
        Recalculates and updates the wallet balance based on
        completed transactions.
        Args:
            wallet (Wallet): The wallet instance to recalculate balance for.
        Returns:
            Decimal: The updated wallet balance.
        """
        try:
            query_filter = (
                (Q(transaction_type="CASH_IN") | Q(transaction_type="PAYOUT")) &
                Q(status="COMPLETED")
            )
            total = (wallet.transactions.filter(query_filter).aggregate(
                total=Sum("amount"))["total"] or 0)
        except AttributeError:
            raise WalletError("Wallet error")

        wallet.balance = total
        wallet.save(update_fields=["balance"])

        return wallet.balance
