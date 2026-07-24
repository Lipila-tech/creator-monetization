# This module defines utility functions that send
# vairious emails to users. These functions can be called from views, 
# signals, or Celery tasks. 
# Types of emails
# - Missing payout account email: Sent to creators who have a pending payout but no payout account set up.
# - Transaction receipt email: Sent to users after they receive a donation, containing transaction details.
# - Daily/weekly summary email: Sent to creators summarizing their earnings and activity over a period of time (future feature).

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import logging
from django.db.models import QuerySet

logger = logging.getLogger(__name__)


def send_missing_payout_account_email(wallet):
    """
    Send an email to a creator requesting them to set up a payout account.
    
    Used when there's a pending payout but no payout account is configured.
    
    Args:
        wallet (Wallet): The wallet object of the creator
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        creator_user = wallet.creator.user
        subject = "Action Required: Set Up Your Payout Account"
        
        # Plain text version
        message = f"""
Hello {creator_user.first_name or creator_user.username},

We are writing to inform you that an administrator is attempting to process a payout
for your account. However, we were unable to complete the payout because you have not
yet set up a payout account.

To receive your earnings, please:
1. Log into your creator dashboard
2. Navigate to your wallet settings
3. Add your payout account details (mobile money provider, account name, and phone number)

Once you've set up your payout account, the admin can proceed with the payout.

If you have any questions or need assistance, please don't hesitate to contact our support team.

Best regards,
TipZed Admin Team
        """
        
        # HTML version
        html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <div style="background-color: #667eea; padding: 20px; border-radius: 8px 8px 0 0; color: white;">
                <h2 style="margin: 0;">Action Required: Set Up Your Payout Account</h2>
            </div>
            
            <div style="padding: 20px;">
                <p>Hello {creator_user.first_name or creator_user.username},</p>
                
                <p>We are writing to inform you that an administrator is attempting to process a payout for your account.
                However, we were unable to complete the payout because you have not yet set up a payout account.</p>
                
                <h3 style="color: #667eea;">To receive your earnings, please:</h3>
                <ol>
                    <li>Log into your creator dashboard</li>
                    <li>Navigate to your wallet settings</li>
                    <li>Add your payout account details (mobile money provider, account name, and phone number)</li>
                </ol>
                
                <p>Once you've set up your payout account, the admin can proceed with the payout.</p>
                
                <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
                
                <p style="margin-top: 30px; color: #666; border-top: 1px solid #e0e0e0; padding-top: 20px;">
                    Best regards,<br>
                    <strong>TipZed Admin Team</strong>
                </p>
            </div>
        </div>
    </body>
</html>
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@tipzed.space',
            recipient_list=[creator_user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Successfully sent payout account setup email to {creator_user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send payout account email for wallet {wallet.id}: {str(e)}")
        return False


def send_transaction_receipt_email(payment, recipient_email=None):
    """
    Send a transaction receipt email to a user after they've sent a donation.
    
    Contains transaction details, amount, creator information, and receipt reference.
    
    Args:
        payment (Payment): The payment/transaction object
        recipient_email (str, optional): Email address to send to. If None, uses payment.patron_email
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Use provided email or fall back to payment's patron email
        email = recipient_email or payment.patron_email
        
        if not email:
            logger.warning(f"No recipient email found for payment {payment.reference}")
            return False
        
        # Get creator info from wallet
        creator = payment.wallet.creator
        creator_user = creator.user
        
        # Format currency display
        currency_display = dict(payment._meta.get_field('currency').choices).get(
            payment.currency, payment.currency
        )
        
        # Calculate provider fee display
        provider_fee = payment.provider_fee or Decimal('0.00')
        net_amount = payment.net_amount or (payment.amount - provider_fee)
        
        subject = f"TipZed Receipt: Your donation to {creator_user.get_full_name() or creator_user.username}"
        
        # Plain text version
        message = f"""
Hello {payment.patron_name or 'Valued Supporter'},

Thank you for your support! We've received your donation.

Transaction Details:
Reference: {payment.reference}
Amount: {payment.amount} {payment.currency}
Status: {payment.get_status_display()}
Date: {payment.created_at.strftime('%B %d, %Y at %I:%M %p')}

Creator: {creator_user.get_full_name() or creator_user.username}
Message: {payment.patron_message or 'No message included'}

Your support helps creators continue doing what they love.
You can view this transaction in your TipZed account anytime.

Thank you for being awesome!

Best regards,
TipZed Team
        """
        
        # HTML version
        status_color = '#4CAF50' if payment.status in ['completed', 'captured'] else '#FF9800'
        html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <div style="background-color: #667eea; padding: 20px; border-radius: 8px 8px 0 0; color: white; text-align: center;">
                <h2 style="margin: 0;">TipZed Receipt</h2>
                <p style="margin: 10px 0 0 0; font-size: 14px;">Thank you for your support!</p>
            </div>
            
            <div style="padding: 20px;">
                <p>Hello {payment.patron_name or 'Valued Supporter'},</p>
                
                <p>Thank you for your support! We've received your donation to 
                <strong>{creator_user.get_full_name() or creator_user.username}</strong>.</p>
                
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #667eea;">Transaction Details</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Reference:</td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0;">{payment.reference}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Amount:</td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0;">
                                <strong style="font-size: 18px; color: #667eea;">{payment.amount} {payment.currency}</strong>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Status:</td>
                            <td style="padding: 8px 0; border-bottom: 1px solid #e0e0e0;">
                                <span style="background-color: {status_color}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                                    {payment.get_status_display()}
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Date:</td>
                            <td style="padding: 8px 0;">{payment.created_at.strftime('%B %d, %Y at %I:%M %p')}</td>
                        </tr>
                    </table>
                </div>
                
                <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0;">
                    <p><strong>Creator:</strong> {creator_user.get_full_name() or creator_user.username}</p>
                    <p><strong>Your Message:</strong></p>
                    <p style="margin: 10px 0; font-style: italic; color: #666;">
                        "{payment.patron_message or 'No message included'}"
                    </p>
                </div>
                
                <p>Your support helps creators continue doing what they love. You can view this transaction 
                in your TipZed account anytime.</p>
                
                <p style="margin-top: 30px; color: #666; border-top: 1px solid #e0e0e0; padding-top: 20px;">
                    Thank you for being awesome!<br>
                    <strong>TipZed Team</strong>
                </p>
            </div>
        </div>
    </body>
</html>
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@tipzed.space',
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Successfully sent transaction receipt email to {email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send transaction receipt email for payment {payment.reference}: {str(e)}")
        return False


def send_daily_weekly_summary_email(wallet, period='daily'):
    """
    Send a summary email to a creator with their earnings and activity.
    
    Future feature: Sends daily, weekly, or custom period summaries with:
    - Total earnings during period
    - Number of donations received
    - Average donation amount
    - Top supporters
    - Activity trend insights
    
    Args:
        wallet (Wallet): The wallet object of the creator
        period (str): 'daily', 'weekly', or 'custom' (default: 'daily')
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        creator_user = wallet.creator.user
        
        # Calculate the date range based on period
        now = timezone.now()
        if period == 'daily':
            start_date = now - timedelta(days=1)
            period_label = "Today"
        elif period == 'weekly':
            # Last 7 days
            start_date = now - timedelta(days=7)
            period_label = "This Week"
        else:
            # Default to daily
            start_date = now - timedelta(days=1)
            period_label = "Custom Period"
        
        # Get transactions for the period
        transactions = wallet.transactions.filter(
            created_at__gte=start_date,
            transaction_type='CASH_IN',
            status='COMPLETED'
        )
        
        # Calculate statistics
        total_earnings = Decimal('0.00')
        total_tips = 0
        total_fees = Decimal('0.00')
        
        for transaction in transactions:
            total_earnings += transaction.amount
            total_fees += transaction.fee
            total_tips += 1
        
        average_tip = total_earnings / total_tips if total_tips > 0 else Decimal('0.00')
        
        # Get recent supporters/payments
        from apps.payments.models import Payment
        payments = Payment.objects.filter(
            wallet=wallet,
            created_at__gte=start_date,
            status__in=['completed', 'captured']
        ).order_by('-created_at')[:5]
        
        subject = f"TipZed Summary: Your {period_label} Earnings"
        
        # Build supporters list HTML
        supporters_html = ""
        if payments.exists():
            supporters_html = "<h3 style='color: #667eea;'>Recent Tips:</h3><ul>"
            for payment in payments:
                supporter_name = payment.patron_name or 'Anonymous Supporter'
                supporters_html += f"""
                <li style="padding: 10px 0; border-bottom: 1px solid #e0e0e0;">
                    <strong>{supporter_name}</strong> sent {payment.amount} {payment.currency}
                    <br><small style="color: #999;">{payment.created_at.strftime('%B %d at %I:%M %p')}</small>
                </li>
                """
            supporters_html += "</ul>"
        
        # Plain text version
        message = f"""
Hello {creator_user.first_name or creator_user.username},

Here's a summary of your TipZed earnings for {period_label}:

Summary Statistics:
Total Earnings: {total_earnings} {wallet.currency}
Number of Donations: {total_tips}
Average Donation: {average_tip} {wallet.currency}
Total Fees: {total_fees} {wallet.currency}
Current Balance: {wallet.balance} {wallet.currency}

Keep creating amazing content, and your supporters will keep donating!

Best regards,
TipZed Team
        """
        
        # HTML version
        html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <div style="background-color: #667eea; padding: 20px; border-radius: 8px 8px 0 0; color: white; text-align: center;">
                <h2 style="margin: 0;">TipZed Earnings Summary</h2>
                <p style="margin: 10px 0 0 0; font-size: 14px;">{period_label}</p>
            </div>
            
            <div style="padding: 20px;">
                <p>Hello {creator_user.first_name or creator_user.username},</p>
                
                <p>Here's a summary of your TipZed earnings for <strong>{period_label}</strong>:</p>
                
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #667eea;">Summary Statistics</h3>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="background-color: #e8eef7;">
                            <td style="padding: 12px; font-weight: bold; border-radius: 4px 0 0 0;">Total Earnings</td>
                            <td style="padding: 12px; text-align: right; font-size: 20px; color: #667eea; font-weight: bold; border-radius: 0 4px 0 0;">
                                {total_earnings} {wallet.currency}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Number of Donations:</td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">{total_tips}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Average Donation:</td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">{average_tip} {wallet.currency}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; font-weight: bold;">Total Fees:</td>
                            <td style="padding: 12px 0; border-bottom: 1px solid #e0e0e0; text-align: right;">{total_fees} {wallet.currency}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 0; font-weight: bold;">Current Balance:</td>
                            <td style="padding: 12px 0; text-align: right; font-weight: bold; color: #4CAF50;">
                                {wallet.balance} {wallet.currency}
                            </td>
                        </tr>
                    </table>
                </div>
                
                {supporters_html}
                
                <div style="background-color: #f0f7ff; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0; border-radius: 4px;">
                    <p style="margin: 0;">
                        <strong>💡 Pro Tip:</strong> Keep creating amazing content, and your supporters will keep donating! 
                        Your dedication to your craft is what makes TipZed special.
                    </p>
                </div>
                
                <p style="margin-top: 30px; color: #666; border-top: 1px solid #e0e0e0; padding-top: 20px;">
                    Best regards,<br>
                    <strong>TipZed Team</strong>
                </p>
            </div>
        </div>
    </body>
</html>
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@tipzed.space',
            recipient_list=[creator_user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Successfully sent {period} summary email to {creator_user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send summary email for wallet {wallet.id}: {str(e)}")
        return False


def send_welcome_email(user):
    """
    Send a welcome email to a newly signed up creator.
    
    Sent when a creator account is created, welcoming them to the platform
    and providing getting started information.
    
    Args:
        user (CustomUser): The newly created creator user object
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = "Welcome to TipZed! 🎉 Let's Get You Started"
        
        # Plain text version
        message = f"""
Hello {user.first_name or user.username},

Welcome to TipZed! We're thrilled to have you join our creative community.

You're now part of a platform where your supporters can easily send you tips
to show their appreciation for the amazing content you create.

Getting Started:
1. Complete Your Creator Profile
   - Add a profile picture and cover image
   - Write a bio describing what you do

2. Set Up Your Wallet
   - Link your mobile money account (MTN, Airtel, Zamtel)
   - Enable automatic payouts if desired
   - Track your earnings in real-time

3. Share Your Creator Link
   - Promote your unique creator page to your audience
   - Each donation supports your creative work directly
   - Engage with your supporters and thank them

Tips for Success:
- Keep your profile up to date
- Respond to your supporters' messages
- Create consistent, quality content
- Share your earnings milestones to celebrate with your community

If you have any questions or need assistance, our support team is here to help.
Don't hesitate to reach out!

Happy creating!

Best regards,
The TipZed Team
Email: tipzed2@gmail.com
        """
        
        # HTML version
        html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 700px; margin: 0 auto; padding: 0;">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center; color: white; border-radius: 8px 8px 0 0;">
                <h1 style="margin: 0; font-size: 28px;">🎉 Welcome to TipZed!</h1>
                <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Earning Made Easy</p>
            </div>
            
            <!-- Main Content -->
            <div style="background-color: #fff; padding: 40px 20px; border: 1px solid #e0e0e0; border-top: none;">
                <p>Hello {user.first_name or user.username},</p>
                
                <p style="font-size: 16px; color: #666;">
                    Welcome to TipZed! We're thrilled to have you join our creative community.
                </p>
                
                <p style="font-size: 16px; color: #666;">
                    You're now part of a platform where your supporters can easily send you tips
                    to show their appreciation for the amazing content you create.
                </p>
                
                <!-- Getting Started Section -->
                <h2 style="color: #667eea; margin-top: 30px; margin-bottom: 20px; border-bottom: 2px solid #667eea; padding-bottom: 10px;">
                    Getting Started
                </h2>
                
                <div style="margin: 20px 0;">
                    <div style="background-color: #f9f9f9; padding: 15px; margin-bottom: 15px; border-left: 4px solid #667eea; border-radius: 4px;">
                        <h3 style="margin: 0 0 8px 0; color: #667eea;">1. Complete Your Creator Profile</h3>
                        <ul style="margin: 8px 0; color: #666;">
                            <li>Add a profile picture and cover image</li>
                            <li>Write a bio describing what you do</li>
                        </ul>
                    </div>
                    
                    <div style="background-color: #f9f9f9; padding: 15px; margin-bottom: 15px; border-left: 4px solid #667eea; border-radius: 4px;">
                        <h3 style="margin: 0 0 8px 0; color: #667eea;">2. Set Up Your Wallet</h3>
                        <ul style="margin: 8px 0; color: #666;">
                            <li>Link your mobile money account (MTN, Airtel, Zamtel)</li>
                            <li>Enable automatic payouts if desired</li>
                            <li>Track your earnings in real-time</li>
                        </ul>
                    </div>
                    
                    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #667eea; border-radius: 4px;">
                        <h3 style="margin: 0 0 8px 0; color: #667eea;">3. Share Your Creator Link</h3>
                        <ul style="margin: 8px 0; color: #666;">
                            <li>Promote your unique creator page to your audience</li>
                            <li>Each donation supports your creative work directly</li>
                            <li>Engage with your supporters and thank them</li>
                        </ul>
                    </div>
                </div>
                
                <!-- Tips Section -->
                <div style="background-color: #f0f7ff; padding: 20px; border-radius: 8px; margin: 30px 0;">
                    <h3 style="margin-top: 0; color: #667eea;">💡 Tips for Success</h3>
                    <ul style="margin: 10px 0; color: #666; padding-left: 20px;">
                        <li>Keep your profile up to date</li>
                        <li>Respond to your supporters' messages</li>
                        <li>Create consistent, quality content</li>
                        <li>Share your earnings milestones to celebrate with your community</li>
                    </ul>
                </div>
                
                <!-- Support Section -->
                <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                    <p style="margin: 0; color: #856404;">
                        <strong>Need Help?</strong> If you have any questions or need assistance, our support team is here to help.
                        Don't hesitate to reach out!
                    </p>
                </div>
                
                <p style="margin-top: 30px; text-align: center; color: #999; font-size: 14px;">
                    <strong>Happy creating!</strong>
                </p>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f5f5f5; padding: 20px; text-align: center; color: #666; font-size: 13px; border-radius: 0 0 8px 8px; border: 1px solid #e0e0e0; border-top: none;">
                <p style="margin: 0;">
                    Best regards,<br>
                    <strong>The TipZed Team</strong>
                    <strong> Email: tipzed2@gmail.com</strong>
                </p>
                <p style="margin: 10px 0 0 0; color: #999;">
                    TipZed - Empower Creators, Support Creativity
                </p>
            </div>
        </div>
    </body>
</html>
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@tipzed.space',
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Successfully sent welcome email to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send welcome email for user {user.id}: {str(e)}")
        return False


def send_reminder_to_share_creator_link_email(wallets: QuerySet):
    """
    Send a reminder email to a creator who has zero balance to share their support link.
    
    This can be triggered by a Celery beat task that runs daily and checks for creators who
    have received tips but haven't shared their creator link.

    Args: wallets (QuerySet): QuerySet of Wallet objects that meet the criteria for
        receiving the reminder email

    """
    for wallet in wallets:
        try:
            creator_user = wallet.creator.user

            subject = "Share Your Creator Link and Get More Tips!"
            message = f"""Hello {creator_user.first_name or creator_user.username},
                            We noticed that you've received some tips, but you haven't shared your
                            creator link yet. Sharing your link is the best way to get more support
                            from your audience!
                            Here's how to share your creator link:
                            1. Log into your creator dashboard
                            2. Copy your unique creator link
                            3. Share it on your social media, website, or with your fans
                            The more you share, the more tips you can receive! If you need any help,
                            feel free to reach out to our support team.
                            Best regards,
                            The TipZed Team
            """
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@tipzed.space',
                recipient_list=[creator_user.email],
                fail_silently=False,
            )
            logger.info(f"Successfully sent reminder email to {creator_user.email}")
        except Exception as e:
            logger.error(f"Failed to send reminder email: {str(e)}")


def welcome_early_adopter_email(email: str) -> bool:
    """
    Sends a welcome email to ealry adopters and tells them the benefits

    Args: email (str): Unique email address belonging to a creator to send an email to.
    """
    try:
        subject = "Welcome to TipZed! 🎉 Exclusive Benefits for Early Adopters"
        message = f"""Hello,

        Welcome to TipZed! As one of our early adopters, you're part of an exclusive group of creators who are shaping the future of our platform. We're thrilled to have you on board and want to share some of the special benefits you can enjoy as an early adopter:

        1. Priority Support: Get access to our dedicated support team for any questions or assistance you may need.
        2. Feature Previews: Be the first to try out new features and provide feedback that will help us improve.
        3. Community Recognition: Join our early adopter community and connect with other creators who are also part of this exciting journey.
        4. Exclusive Resources: Access guides, tips, and best practices to help you maximize your success on TipZed.

        We're committed to supporting you every step of the way as you grow your presence on TipZed. If you have any questions or need assistance, please don't hesitate to reach out.

        Best regards,
        The TipZed Team
        Email: tipzed2@gmail.com
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@tipzed.space',
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent welcome email to early adopter {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to early adopter {email}: {str(e)}")
        return False


def send_reminder_to_complete_profile(email: str) -> bool:
    """
    Send a reminder email to a creator who have not unverified profiles.
    
    This can be triggered by a Celery beat task that runs daily and checks for creators who
    have signed up but haven't completed their profile.

    Args: emails (list): List of email addresses belonging to creators to send an email to.
    """
    try:
        subject = "Complete Your TipZed Profile and Start Earning!"
        message = f"""Hello,

        We noticed that you haven't completed your TipZed profile setup yet. Completing your profile is essential to start receiving tips from your supporters. Here's how you can complete your profile:

        1. Log into your creator dashboard
        2. Add a profile picture and cover image
        3. Write a compelling bio about yourself and your content
        4. Set up your wallet to receive payouts

        The more complete your profile, the more likely supporters will be to support you! If you need any help, feel free to reach out to our support team.

        Best regards,
        The TipZed Team
        Email: tipzed2@gmail.com
        """
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@tipzed.space',
            recipient_list=[email],
            fail_silently=False,
        )
        logger.info(f"Successfully sent reminder email to {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send reminder email: {str(e)}")
        return False