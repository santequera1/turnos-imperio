# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TurnosConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def recibir_notificacion(self, event):
        mensaje = event['mensaje']

        # Enviar el mensaje al cliente
        await self.send(text_data=json.dumps({
            'mensaje': mensaje
        }))
