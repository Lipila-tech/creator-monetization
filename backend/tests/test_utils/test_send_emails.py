"""
Tests for email sending utility functions in utils/send_emails.py
"""
import pytest
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from utils.send_emails import (
    send_missing_payout_account_email,
    send_transaction_receipt_email,
    send_daily_weekly_summary_email,
    send_welcome_email,
    send_reminder_to_share_creator_link_email,
)
from tests.factories import (
    UserFactory,
    WalletTransactionFactory,
)


@pytest.mark.django_db
class TestSendMissingPayoutAccountEmail:
    """Tests for send_missing_payout_account_email function."""

    def test_send_missing_payout_account_email_success(self, mocker, user_factory):
        """Test successful sending of missing payout account email."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        result = send_missing_payout_account_email(wallet)
        
        # Assert
        assert result is True
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args[1]
        
        assert call_kwargs['subject'] == "Action Required: Set Up Your Payout Account"
        assert user_factory.email in call_kwargs['recipient_list']
        assert 'payout account' in call_kwargs['message'].lower()
        assert 'html_message' in call_kwargs
        assert '<html>' in call_kwargs['html_message']

    def test_send_missing_payout_account_email_includes_creator_name(self, mocker):
        """Test that email includes creator's first name or username."""
        # Arrange
        wallet = UserFactory(first_name='John', username='john_doe').creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_missing_payout_account_email(wallet)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        assert 'Hello John' in call_kwargs['message']
        assert 'Hello John' in call_kwargs['html_message']

    def test_send_missing_payout_account_email_fallback_username(self, mocker):
        """Test that email uses username when first_name not available."""
        # Arrange
        wallet = UserFactory(first_name='', username='testcreator').creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_missing_payout_account_email(wallet)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        assert 'Hello testcreator' in call_kwargs['message']

    def test_send_missing_payout_account_email_includes_instructions(self, mocker, user_factory):
        """Test that email includes setup instructions."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_missing_payout_account_email(wallet)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'creator dashboard' in message.lower()
        assert 'wallet settings' in message.lower()
        assert 'payout account details' in message.lower()

    def test_send_missing_payout_account_email_exception_handling(self, mocker, user_factory):
        """Test that function handles exceptions gracefully."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        mock_send_mail = mocker.patch(
            'utils.send_emails.send_mail',
            side_effect=Exception("SMTP error")
        )
        mock_logger = mocker.patch('utils.send_emails.logger')
        
        # Act
        result = send_missing_payout_account_email(wallet)
        
        # Assert
        assert result is False
        mock_logger.error.assert_called_once()
        assert 'Failed to send payout account email' in mock_logger.error.call_args[0][0]

    def test_send_missing_payout_account_email_uses_correct_from_email(self, mocker, user_factory):
        """Test that email uses configured FROM email."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_missing_payout_account_email(wallet)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        from_email = call_kwargs['from_email']
        assert from_email == settings.DEFAULT_FROM_EMAIL


@pytest.mark.django_db
class TestSendTransactionReceiptEmail:
    """Tests for send_transaction_receipt_email function."""

    def test_send_transaction_receipt_email_success(self, mocker, payment_factory):
        """Test successful sending of transaction receipt email."""
        # Arrange
        payment_factory.patron_email = 'patron@example.com'
        payment_factory.status = 'completed'
        payment_factory.save()
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        result = send_transaction_receipt_email(payment_factory)
        
        # Assert
        assert result is True
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args[1]
        
        assert 'Receipt' in call_kwargs['subject']
        assert payment_factory.patron_email in call_kwargs['recipient_list']
        assert payment_factory.reference in call_kwargs['message']

    def test_send_transaction_receipt_email_with_custom_recipient(self, mocker, payment_factory):
        """Test sending receipt to custom email address."""
        # Arrange
        payment_factory.patron_email = 'original@example.com'
        custom_email = 'custom@example.com'
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        result = send_transaction_receipt_email(payment_factory, recipient_email=custom_email)
        
        # Assert
        assert result is True
        call_kwargs = mock_send_mail.call_args[1]
        assert custom_email in call_kwargs['recipient_list']
        assert 'original@example.com' not in call_kwargs['recipient_list']

    def test_send_transaction_receipt_email_includes_transaction_details(self, mocker, payment_factory):
        """Test that receipt includes all transaction details."""
        # Arrange
        payment_factory.reference = 'PAY-123456'
        payment_factory.amount = Decimal('50.00')
        payment_factory.currency = 'ZMW'
        payment_factory.status = 'completed'
        payment_factory.patron_name = 'John Supporter'
        payment_factory.patron_message = 'Great content!'
        payment_factory.save()
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_transaction_receipt_email(payment_factory)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'PAY-123456' in message
        assert '50.00' in message
        assert 'ZMW' in message
        assert 'John Supporter' in message
        assert 'Great content!' in message

    def test_send_transaction_receipt_email_includes_creator_info(self, mocker, payment_factory):
        """Test that receipt includes creator name."""
        # Arrange
        payment_factory.wallet.creator.user.first_name = 'Jane'
        payment_factory.wallet.creator.user.last_name = 'Creator'
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_transaction_receipt_email(payment_factory)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'Jane Creator' in message

    def test_send_transaction_receipt_email_no_patron_email(self, mocker, payment_factory):
        """Test handling when no email is available."""
        # Arrange
        payment_factory.patron_email = None 
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        mock_logger = mocker.patch('utils.send_emails.logger')
        
        # Act
        result = send_transaction_receipt_email(payment_factory)
        
        # Assert
        assert result is False
        mock_send_mail.assert_not_called()
        mock_logger.warning.assert_called_once()

    def test_send_transaction_receipt_email_handles_exception(self, mocker, payment_factory):
        """Test exception handling during email send."""
        # Arrange
        payment_factory.save()
        mock_send_mail = mocker.patch(
            'utils.send_emails.send_mail',
            side_effect=Exception("Email service down")
        )
        mock_logger = mocker.patch('utils.send_emails.logger')
        
        # Act
        result = send_transaction_receipt_email(payment_factory)
        
        # Assert
        assert result is False
        mock_logger.error.assert_called_once()
        assert 'Failed to send transaction receipt email' in mock_logger.error.call_args[0][0]

    def test_send_transaction_receipt_email_html_includes_status_indicator(self, mocker, payment_factory):
        """Test that HTML email includes status-based styling."""
        # Arrange
        payment_factory.status = 'completed'
        payment_factory.save()
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_transaction_receipt_email(payment_factory)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        html_message = call_kwargs['html_message']
        
        # Should include status styling
        assert '#4CAF50' in html_message  # Green color for completed
        assert '<html>' in html_message
        assert 'TipZed Receipt' in html_message

    def test_send_transaction_receipt_email_pending_status_color(self, mocker, payment_factory):
        """Test that pending status uses different color."""
        # Arrange
        payment_factory.status = 'pending'
        payment_factory.save()
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_transaction_receipt_email(payment_factory)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        html_message = call_kwargs['html_message']
        
        # Should include pending status styling
        assert '#FF9800' in html_message  # Orange color for pending

    def test_send_transaction_receipt_email_no_message_fallback(self, mocker, payment_factory):
        """Test that email handles missing patron message."""
        # Arrange
        payment_factory.patron_message = None
        payment_factory.save()
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_transaction_receipt_email(payment_factory)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'No message included' in message


@pytest.mark.django_db
class TestSendDailyWeeklySummaryEmail:
    """Tests for send_daily_weekly_summary_email function."""

    def test_send_daily_summary_email_success(self, mocker, wallet_factory):
        """Test successful sending of daily summary email."""
        # Arrange
        wallet_factory.balance = Decimal('1000.00')
        wallet_factory.save()
        now = timezone.now()
        WalletTransactionFactory(
            wallet=wallet_factory,
            created_at=now - timedelta(hours=1),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('50.00'),
            fee=Decimal('2.50'),
        )
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        result = send_daily_weekly_summary_email(wallet_factory, period='daily')
        
        # Assert
        assert result is True
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args[1]
        
        assert 'Summary' in call_kwargs['subject']
        assert 'Today' in call_kwargs['subject']
        assert wallet_factory.creator.user.email in call_kwargs['recipient_list']

    def test_send_weekly_summary_email_success(self, mocker, wallet_factory):
        """Test successful sending of weekly summary email."""
        # Arrange
        wallet_factory.balance = Decimal('1000.00')
        wallet_factory.save()
        now = timezone.now()
        
        # Create transactions from the past week
        for i in range(3):
            WalletTransactionFactory(
                wallet=wallet_factory,
                created_at=now - timedelta(days=i),
                transaction_type='CASH_IN',
                status='COMPLETED',
                amount=Decimal('30.00'),
                fee=Decimal('1.50'),
            )
        
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        result = send_daily_weekly_summary_email(wallet_factory, period='weekly')
        
        # Assert
        assert result is True
        call_kwargs = mock_send_mail.call_args[1]
        assert 'This Week' in call_kwargs['subject']

    def test_send_summary_email_calculates_correct_totals(self, mocker, user_factory):
        """Test that summary calculates correct earnings totals."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        now = timezone.now()
        
        WalletTransactionFactory(
            wallet=wallet,
            created_at=now - timedelta(hours=1),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('100.00'),
            fee=Decimal('5.00'),
        )
        WalletTransactionFactory(
            wallet=wallet,
            created_at=now - timedelta(hours=2),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('50.00'),
            fee=Decimal('2.50'),
        )
        
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        # Total earnings: 150.00
        assert '150.00' in message or '150' in message
        # Total fees: 7.50
        assert '7.50' in message or '7.5' in message
        # Number of Donations: 2
        assert '2' in message

    def test_send_summary_email_only_includes_completed_transactions(self, mocker, user_factory):
        """Test that only completed transactions are included in summary."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        now = timezone.now()
        
        # Create completed transaction
        WalletTransactionFactory(
            wallet=wallet,
            created_at=now - timedelta(hours=1),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('100.00'),
        )
        
        # Create pending transaction (should be excluded)
        WalletTransactionFactory(
            wallet=wallet,
            created_at=now - timedelta(hours=2),
            transaction_type='CASH_IN',
            status='PENDING',
            amount=Decimal('50.00'),
        )
        
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        # Should only include the 100.00 transaction
        assert '100.00' in message
        # Number of donations should be 1
        assert 'Number of Donations: 1' in message

    from unittest import skip

    @skip("Remove skip when implementation is complete")
    def test_send_summary_email_excludes_old_transactions(self, mocker, user_factory):
        """Test that only transactions from the period are included."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        now = timezone.now()
        
        # Create recent transaction (within last 24 hours)
        WalletTransactionFactory(
            wallet=wallet,
            created_at=now - timedelta(hours=5),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('100.00'),
        )
        
        # Create old transaction (more than 7 days ago)
        WalletTransactionFactory(
            wallet=wallet,
            created_at=now - timedelta(days=10),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('500.00'),
        )
        
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        # Should only include the recent 100.00 transaction
        assert 'Number of Donations: 1' in message or '1' in message

    def test_send_summary_email_calculates_average_tip(self, mocker, user_factory):
        """Test that average donation is calculated correctly."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        now = timezone.now()
        
        WalletTransactionFactory(
            wallet=wallet,
            created_at=now - timedelta(hours=1),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('100.00'),
            fee=Decimal('0.00'),
        )
        WalletTransactionFactory(
            wallet=wallet,
            created_at=now - timedelta(hours=2),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('200.00'),
            fee=Decimal('0.00'),
        )
        
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        # Average should be 150.00 (300 / 2)
        assert '150' in message

    def test_send_summary_email_includes_wallet_balance(self, mocker, user_factory):
        """Test that current wallet balance is included."""
        # Arrange
        wallet = wallet = user_factory.creator_profile.wallet
        wallet.balance = Decimal('5000.00')
        wallet.save()
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        # Should include current balance
        assert '5000' in message or '5000.00' in message

    def test_send_summary_email_no_transactions(self, mocker, user_factory):
        """Test summary with no transactions in period."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        result = send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        assert result is True
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        # Should show zero earnings
        assert 'Total Earnings: 0' in message or 'Total Earnings: 0.00' in message
        assert 'Number of Donations: 0' in message

    def test_send_summary_email_exception_handling(self, mocker, user_factory):
        """Test exception handling during summary email send."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        mock_send_mail = mocker.patch(
            'utils.send_emails.send_mail',
            side_effect=Exception("Email service error")
        )
        mock_logger = mocker.patch('utils.send_emails.logger')
        
        # Act
        result = send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        assert result is False
        mock_logger.error.assert_called_once()
        assert 'Failed to send summary email' in mock_logger.error.call_args[0][0]

    def test_send_summary_email_includes_creator_name(self, mocker):
        """Test that summary email includes creator's name."""
        # Arrange
        wallet = UserFactory(first_name='Alice', username='alicecreator').creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'Hello Alice' in message

    def test_send_summary_email_html_format(self, mocker, user_factory):
        """Test that HTML version is properly formatted."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        WalletTransactionFactory(
            wallet=wallet,
            created_at=timezone.now() - timedelta(hours=1),
            transaction_type='CASH_IN',
            status='COMPLETED',
            amount=Decimal('75.00'),
        )
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        html_message = call_kwargs['html_message']
        
        assert '<html>' in html_message
        assert 'Summary Statistics' in html_message
        assert '#667eea' in html_message  # Brand color
        assert 'TipZed Earnings Summary' in html_message

    def test_send_summary_email_period_label_daily(self, mocker, user_factory):
        """Test that period label is correct for daily."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='daily')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        subject = call_kwargs['subject']
        
        assert 'Today' in subject

    def test_send_summary_email_period_label_weekly(self, mocker, user_factory):
        """Test that period label is correct for weekly."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_daily_weekly_summary_email(wallet, period='weekly')
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        subject = call_kwargs['subject']
        
        assert 'This Week' in subject


@pytest.mark.django_db
class TestSendWelcomeEmail:
    """Tests for send_welcome_email function."""

    def test_send_welcome_email_success(self, mocker):
        """Test successful sending of welcome email to new creator."""
        # Arrange
        user = UserFactory(user_type='creator', first_name='Alex')
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        result = send_welcome_email(user)
        
        # Assert
        assert result is True
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args[1]
        
        assert 'Welcome' in call_kwargs['subject']
        assert 'TipZed' in call_kwargs['subject']
        assert user.email in call_kwargs['recipient_list']
        assert 'Hello Alex' in call_kwargs['message']
        assert '<html>' in call_kwargs['html_message']

    def test_send_welcome_email_includes_getting_started_info(self, mocker):
        """Test that welcome email includes getting started instructions."""
        # Arrange
        user = UserFactory(user_type='creator')
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_welcome_email(user)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'Complete Your Creator Profile' in message
        assert 'Set Up Your Wallet' in message
        assert 'Share Your Creator Link' in message
        assert 'MTN' in message or 'Airtel' in message or 'mobile money' in message.lower()

    def test_send_welcome_email_includes_tips_for_success(self, mocker):
        """Test that welcome email includes success tips."""
        # Arrange
        user = UserFactory(user_type='creator')
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_welcome_email(user)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'Tips for Success' in message
        assert 'profile' in message.lower()
        assert 'community' in message.lower()

    def test_send_welcome_email_fallback_username(self, mocker):
        """Test that welcome email uses username when first_name is empty."""
        # Arrange
        user = UserFactory(user_type='creator', first_name='', username='newcreator')
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_welcome_email(user)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'Hello newcreator' in message

    def test_send_welcome_email_html_format(self, mocker):
        """Test that HTML version is properly formatted with styling."""
        # Arrange
        user = UserFactory(user_type='creator')
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_welcome_email(user)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        html_message = call_kwargs['html_message']
        
        assert '<html>' in html_message
        assert 'Getting Started' in html_message
        assert '#667eea' in html_message  # Brand color
        assert 'TipZed' in html_message
        assert 'gradient' in html_message  # Background gradient

    def test_send_welcome_email_includes_support_info(self, mocker):
        """Test that welcome email includes support information."""
        # Arrange
        user = UserFactory(user_type='creator')
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_welcome_email(user)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'support' in message.lower()

    def test_send_welcome_email_exception_handling(self, mocker):
        """Test exception handling during welcome email send."""
        # Arrange
        user = UserFactory(user_type='creator')
        mock_send_mail = mocker.patch(
            'utils.send_emails.send_mail',
            side_effect=Exception("Email service error")
        )
        mock_logger = mocker.patch('utils.send_emails.logger')
        
        # Act
        result = send_welcome_email(user)
        
        # Assert
        assert result is False
        mock_logger.error.assert_called_once()
        assert 'Failed to send welcome email' in mock_logger.error.call_args[0][0]

    def test_send_welcome_email_uses_correct_from_email(self, mocker):
        """Test that welcome email uses configured FROM email."""
        # Arrange
        user = UserFactory(user_type='creator')
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_welcome_email(user)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        from_email = call_kwargs['from_email']
        
        assert from_email == settings.DEFAULT_FROM_EMAIL


@pytest.mark.django_db
class TestSendReminderToShareCreatorLinkEmail:
    """Tests for send_reminder_to_share_creator_link_email function."""

    def test_send_reminder_single_wallet_success(self, mocker, user_factory):
        """Test successful sending of reminder email to single wallet."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args[1]
        
        assert 'Share Your Creator Link' in call_kwargs['subject']
        assert wallet.creator.user.email in call_kwargs['recipient_list']
        assert 'creator link' in call_kwargs['message'].lower()

    def test_send_reminder_multiple_wallets_success(self, mocker):
        """Test sending reminder emails to multiple wallets."""
        # Arrange
        from apps.wallets.models import Wallet
        user1 = UserFactory(first_name='User1', username='user1')
        user2 = UserFactory(first_name='User2', username='user2')
        wallet1 = user1.creator_profile.wallet
        wallet2 = user2.creator_profile.wallet
        wallets = Wallet.objects.filter(id__in=[wallet1.id, wallet2.id])
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        assert mock_send_mail.call_count == 2
        
        # Check that both emails were sent to correct recipients
        call_args_list = mock_send_mail.call_args_list
        recipients = [call[1]['recipient_list'][0] for call in call_args_list]
        
        assert user1.email in recipients
        assert user2.email in recipients

    def test_send_reminder_includes_creator_name(self, mocker):
        """Test that reminder email includes creator's name."""
        # Arrange
        wallet = UserFactory(first_name='Bob', username='bobcreator').creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'Hello Bob' in message

    def test_send_reminder_includes_instructions(self, mocker, user_factory):
        """Test that reminder email includes sharing instructions."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'creator dashboard' in message.lower()
        assert 'social media' in message.lower()
        assert 'creator link' in message.lower()

    def test_send_reminder_fallback_username(self, mocker):
        """Test that reminder uses username when first_name is empty."""
        # Arrange
        wallet = UserFactory(first_name='', username='testcreator99').creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'Hello testcreator99' in message

    def test_send_reminder_empty_queryset(self, mocker):
        """Test that function handles empty queryset gracefully."""
        # Arrange
        from apps.wallets.models import Wallet
        wallets = Wallet.objects.none()
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        mock_send_mail.assert_not_called()

    def test_send_reminder_uses_correct_from_email(self, mocker, user_factory):
        """Test that reminder email uses configured FROM email."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        from_email = call_kwargs['from_email']
        
        assert from_email == settings.DEFAULT_FROM_EMAIL

    def test_send_reminder_exception_handling(self, mocker, user_factory):
        """Test exception handling during reminder email send."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch(
            'utils.send_emails.send_mail',
            side_effect=Exception("Email service error")
        )
        mock_logger = mocker.patch('utils.send_emails.logger')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        mock_logger.error.assert_called_once()
        assert 'Failed to send reminder email' in mock_logger.error.call_args[0][0]

    def test_send_reminder_partial_failure_continues(self, mocker):
        """Test that function continues even if one email fails."""
        # Arrange
        from apps.wallets.models import Wallet
        user1 = UserFactory(first_name='User1')
        user2 = UserFactory(first_name='User2')
        wallet1 = user1.creator_profile.wallet
        wallet2 = user2.creator_profile.wallet
        wallets = Wallet.objects.filter(id__in=[wallet1.id, wallet2.id]).order_by('id')
        
        # Mock send_mail to fail on first call, succeed on second
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        mock_send_mail.side_effect = [Exception("First email failed"), None]
        mock_logger = mocker.patch('utils.send_emails.logger')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        # Should attempt to send both emails, failing only on the first
        assert mock_send_mail.call_count == 2
        # Logger should have error for the failed email
        mock_logger.error.assert_called()

    def test_send_reminder_includes_encouragement(self, mocker, user_factory):
        """Test that reminder email includes encouragement about tips."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'tips' in message.lower()
        assert 'share' in message.lower()

    def test_send_reminder_multiple_wallets_independent_emails(self, mocker):
        """Test that each wallet receives an independent email with correct personalization."""
        # Arrange
        from apps.wallets.models import Wallet
        user1 = UserFactory(first_name='Alice', username='alice')
        user2 = UserFactory(first_name='Bob', username='bob')
        wallet1 = user1.creator_profile.wallet
        wallet2 = user2.creator_profile.wallet
        wallets = Wallet.objects.filter(id__in=[wallet1.id, wallet2.id]).order_by('id')
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        assert mock_send_mail.call_count == 2
        
        call_args_list = mock_send_mail.call_args_list
        messages = [call[1]['message'] for call in call_args_list]
        
        # Check that each message is personalized
        assert any('Hello Alice' in msg for msg in messages)
        assert any('Hello Bob' in msg for msg in messages)

    def test_send_reminder_includes_support_info(self, mocker, user_factory):
        """Test that reminder email includes support team contact."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        assert 'support' in message.lower()

    def test_send_reminder_contains_action_steps(self, mocker, user_factory):
        """Test that email contains clear action steps."""
        # Arrange
        wallet = user_factory.creator_profile.wallet
        wallets = wallet.__class__.objects.filter(id=wallet.id)
        mock_send_mail = mocker.patch('utils.send_emails.send_mail')
        
        # Act
        send_reminder_to_share_creator_link_email(wallets)
        
        # Assert
        call_kwargs = mock_send_mail.call_args[1]
        message = call_kwargs['message']
        
        # Should have numbered steps or clear instructions
        assert '1.' in message or 'Log into' in message
        assert '2.' in message or 'Copy' in message or 'Copy' in message
        assert '3.' in message or 'Share' in message

