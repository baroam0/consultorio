
from django.db import models

from apps.obrassociales.models import ObraSocial
from apps.pacientes.models import Paciente
from apps.profesionales.models import Profesional


class Turno(models.Model):
    fechahora = models.DateTimeField(null=False, blank=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    obrasocial = models.ForeignKey(ObraSocial, on_delete=models.CASCADE)
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    asistio = models.BooleanField(default=False)
    entrega = models.BooleanField(default=False)
    entrega_parcial = models.BooleanField(default=False)
    observacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.fechahora)
    
    class Meta:
        verbose_name_plural = "Turnos"


# Create your models here.
