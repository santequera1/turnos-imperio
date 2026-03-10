from django.db import models
from django.db import models


class Turno(models.Model):
    nombre_cliente = models.CharField(max_length=50)
    referencia_motocicleta = models.CharField(max_length=30)
    numero_telefono = models.CharField(max_length=15)
    motivo_reparacion = models.CharField(max_length=50)
    numero_turno = models.PositiveIntegerField(default=0, editable=False)
    


    def save(self, *args, **kwargs):
        if not self.id:  # Si es un nuevo objeto
            last_turno = Turno.objects.order_by('-numero_turno').first()
            if last_turno:
                self.numero_turno = last_turno.numero_turno + 1
            else:
                self.numero_turno = 1
        super(Turno, self).save(*args, **kwargs)



"""#Modelo Turnos
class Turno(models.Model):
    nombre_cliente = models.CharField(max_length=50)
    referencia_motocicleta = models.CharField(max_length=30)
    numero_telefono = models.CharField(max_length=15)



    def __str__(self):
        return self.nombre_cliente
"""
