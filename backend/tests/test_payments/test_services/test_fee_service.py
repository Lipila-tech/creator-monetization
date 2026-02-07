import pytest
from decimal import Decimal
from apps.payments.services.fee_service import FeeService, InvalidAmount

class TestFeeService:
    def test_calculate_cashin_fee(self):
        fee = FeeService.calculate_cash_in_fee(Decimal("100.00"))
        assert fee == Decimal("10.00")

    def test_method_converts_string_to_decimal(self):
        fee = FeeService.calculate_cash_in_fee("100.00")
        assert fee == Decimal("10.00")

    def test_method_converts_int_to_decimal(self):
        fee = FeeService.calculate_cash_in_fee(100.00)
        assert fee == Decimal("10.00")

    def test_method_converts_float_to_decimal(self):
        fee = FeeService.calculate_cash_in_fee(float(100))
        assert fee == Decimal("10.00")

    def test_handle_non_digit(self):
        with pytest.raises(InvalidAmount, match="Amount must be positive"):
            FeeService.calculate_cash_in_fee('non-number')

    def test_handle_negative_amount(self):
        with pytest.raises(InvalidAmount, match="Amount must be positive"):
            FeeService.calculate_cash_in_fee(Decimal("-4.00"))

    def test_handle_zero_amount(self):
        with pytest.raises(InvalidAmount, match="Amount must be positive"):
            FeeService.calculate_cash_in_fee(Decimal("0.00"))

    def test_calculate_cashin_fee_with_custom_percentage(self):
        fee = FeeService.calculate_cash_in_fee(Decimal("100.00"), charge=50)
        assert fee == Decimal("50.00")

    def test_computes_float_and_decimal(self):
        fee = FeeService.calculate_cash_in_fee(Decimal("100.00"), charge=float(50))
        assert fee == Decimal("50.00")

    def test_computes_percentage_less_than_1(self):
        fee = FeeService.calculate_cash_in_fee(Decimal("100.00"), charge=0.5)
        assert fee == Decimal("0.50")

    def test_program_does_not_crash_when_percentage_is_zero(self):
        with pytest.raises(InvalidAmount, match="Amount must be positive"):
            FeeService.calculate_cash_in_fee(Decimal("100.00"), charge=0)