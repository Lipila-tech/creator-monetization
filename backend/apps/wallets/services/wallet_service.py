from django.db.models import Sum

from apps.wallets.models.payment_related import Wallet
from utils.exceptions import WalletNotFound


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
        except Wallet.DoesNotExist:
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
        total = (
            wallet.transactions.filter(status="COMPLETED").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        wallet.balance = total
        wallet.save(update_fields=["balance"])

        return wallet.balance
