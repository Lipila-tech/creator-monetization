from decimal import Decimal
from utils.exceptions import InvalidAmount

class FeeService:
    PAYOUT_FEE_FLAT = Decimal("0.00")  # K10

    @classmethod
    def calculate_cash_in_fee(cls, amount: Decimal, charge=Decimal("10")) -> Decimal:
        """
        Calculate the cash-in fee based on the amount.
        Args:
            amount (Decimal): The amount to cash in.
            charge (Decimal): The fee(default 10%) to charge on the amount
        Returns:
            Decimal: The calculated cash-in fee.
        """
        import decimal
        try:
            amount = Decimal(amount)
            charge = Decimal(charge)
        except (decimal.InvalidOperation, TypeError):
            raise InvalidAmount("Amount must be positive")
                    
        if Decimal(amount) < Decimal('1') or Decimal(charge) <= Decimal('0'):
            raise InvalidAmount("Amount must be positive")
        
        return (Decimal(amount) * (Decimal(charge)/100)).quantize(Decimal("0.01"))

    @classmethod
    def payout_fee(cls) -> Decimal:
        """
        Get the flat payout fee.
        Returns:
            Decimal: The flat payout fee.
        """
        return cls.PAYOUT_FEE_FLAT
