# services/mpesa_service.py

import requests
from django.conf import settings
from datetime import datetime
import base64

def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(settings.MPESA_API_KEY, settings.MPESA_API_SECRET))
    response_data = response.json()
    return response_data['access_token']

def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode())
    return encoded_string.decode('utf-8'), timestamp

def initiate_mpesa_payment(phone_number, amount, account_reference, transaction_desc):
    access_token = get_mpesa_access_token()
    password, timestamp = generate_password()
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/mpesa/callback/",
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()