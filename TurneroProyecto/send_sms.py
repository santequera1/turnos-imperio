import os
from twilio.rest import Client

def sendsms():
    account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN', '')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to='+573217171562'
    )

    print(message.sid)