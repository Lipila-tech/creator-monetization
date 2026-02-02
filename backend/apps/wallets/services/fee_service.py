from decimal import Decimal


class FeeService:
    CASH_IN_FEE_PERCENT = Decimal("0.03")  # 3%
    PAYOUT_FEE_FLAT = Decimal("10.00")  # K10

    @classmethod
    def calculate_cash_in_fee(cls, amount: Decimal) -> Decimal:
        """
        Calculate the cash-in fee based on the amount.
        Args:
            amount (Decimal): The amount to cash in.
        Returns:
            Decimal: The calculated cash-in fee.
        """
        return (amount * cls.CASH_IN_FEE_PERCENT).quantize(Decimal("0.01"))

    @classmethod
    def payout_fee(cls) -> Decimal:
        """
        Get the flat payout fee.
        Returns:
            Decimal: The flat payout fee.
        """
        return cls.PAYOUT_FEE_FLAT
