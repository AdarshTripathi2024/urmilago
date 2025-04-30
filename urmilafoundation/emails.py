from django.core.mail import send_mail
from django.conf import settings
import random

def send_otp_email(email, otp):
    subject = 'Your OTP Code for subscription'
    message = f'Your OTP for newsletter subscription is: {otp}'
    from_email = None  # uses DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

def generate_otp():
    return str(random.randint(10000, 99999))