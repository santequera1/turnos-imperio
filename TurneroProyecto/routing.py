# routing.py

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/turnos_app/$', consumers.TurnosConsumer.as_asgi()),
]
