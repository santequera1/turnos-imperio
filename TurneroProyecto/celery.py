from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define el proyecto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TurneroProyecto.settings')

app = Celery('TuneroProyecto')

# Lee la configuración de Celery desde las configuraciones de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks en todas las aplicaciones registradas de Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
