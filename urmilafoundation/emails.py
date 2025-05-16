from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging
import random
logger = logging.getLogger(__name__)

def send_otp_email(email, otp):
    subject = 'Your OTP Code for Urmial Foundation Newsletter Subscription'
    text_content = f'Your OTP for newsletter subscription is: {otp}'
    html_content = f'''
        <html>
            <body>
                <p>Hello,</p>
                <p>Your OTP for <strong>newsletter subscription</strong> is:</p>
                <h2 style="color: #2E86C1;">{otp}</h2>
                <p>This OTP is valid for 10 minutes.</p>
                <br>
                <p>Thanks,<br>The Team</p>
            </body>
        </html>
    '''

    from_email = settings.DEFAULT_FROM_EMAIL  # Better than using None
    recipient_list = [email]

    try:
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"OTP email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send OTP email to {email}: {e}")

def generate_otp():
    return str(random.randint(10000, 99999))