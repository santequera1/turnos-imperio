from twilio.rest import Client
from django.conf import settings
from .forms import TurnoForm
from .models import Turno 

def sendsms(numero_telefono, nombre, motocicleta):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    mensaje = "¡Hola " + nombre + " Ya es tu turno"
    
    message = client.messages.create(
        body=mensaje,
        from_='+19285850221',
        to='+57' + numero_telefono
    )

    print(message.sid)
    print(message)

