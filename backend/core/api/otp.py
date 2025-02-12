import random
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()
TWILIO_ACCOUNT_SID=os.getenv("TWILIO_ACCOUNT_SID")

TWILIO_AUTH_TOKEN=os.getenv("TWILIO_AUTH_TOKEN")

TWILIO_PHONE_NUMBER=os.getenv("TWILIO_PHONE_NUMBER")

def generate_otp():
    return str(random.randint(100000, 999999))  # 6-digit OTP

def send_otp_via_sms(phone_number):
    otp = generate_otp()
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    
    return otp 