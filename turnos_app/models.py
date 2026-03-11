from django.db import models


class ClienteFrecuente(models.Model):
    nombre_cliente = models.CharField(max_length=50)
    referencia_motocicleta = models.CharField(max_length=30)
    motivo_reparacion = models.CharField(max_length=50)
    numero_telefono = models.CharField(max_length=15)
    placa = models.CharField(max_length=20, blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True, null=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.numero_telefono}"


class Turno(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    referencia_motocicleta = models.CharField(max_length=100, blank=True, null=True)
    numero_telefono = models.CharField(max_length=15, blank=True, null=True)
    motivo_reparacion = models.TextField(blank=True, null=True)
    cliente_frecuente = models.ForeignKey(ClienteFrecuente, null=True, blank=True, on_delete=models.SET_NULL)

    numero_turno = models.IntegerField(blank=True, null=True)
    orden = models.IntegerField(blank=True, null=True)
    en_reparacion = models.BooleanField(default=False)

    finalizado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_finalizacion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Turno {self.numero_turno} - {self.nombre_cliente}"

    def save(self, *args, **kwargs):
        if not self.numero_turno:
            last_turno = Turno.objects.filter(finalizado=False).order_by('-numero_turno').first()
            self.numero_turno = (last_turno.numero_turno + 1) if last_turno else 1

        if not self.orden:
            last_orden = Turno.objects.filter(finalizado=False).order_by('-orden').first()
            self.orden = (last_orden.orden + 1) if last_orden else 1

        super(Turno, self).save(*args, **kwargs)

    class Meta:
        ordering = ['orden']