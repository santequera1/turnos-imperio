from twilio.rest import Client
from django.conf import settings
from .forms import TurnoForm
from .models import Turno 



def sendsms(numero_telefono, nombre, motocicleta):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
    client = Client(account_sid, auth_token)
    mensaje = "¡Hola " + nombre + "! Tienes un turno asignado en Imperio Motos para tu motocicleta: " + motocicleta
    
    message = client.messages.create(
        body=mensaje,
        from_='whatsapp:+14155238886',
        to='whatsapp:+57' + numero_telefono
    )

    print(message.sid)
    print(message)
