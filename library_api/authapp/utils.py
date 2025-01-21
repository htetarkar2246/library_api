import random
from django.core.mail import send_mail
import os 

def generate_otp():
  return str(random.randint(100000,999999))

def send_otp_email(receiver_email, otp_code):
  # name of businees from .env 
  business_name = os.getenv("NAME_OF_BUSINESS")
  subject =f"Password Reset OTP from {business_name}."
  # None uses DEFAULT_FROM_EMAIL as the sender_email
  sender_email = None 
  message = f"Hello!!, This message is from {business_name}.\n\nYour OTP code for resetting password is: {otp_code}\n\nThis code will expire in 5 minutes."
  send_mail(subject, message, sender_email, [receiver_email])
  
  