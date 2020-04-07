from django.contrib.auth.models import User
from django.db import models

class Especialidad(models.Model):
    descripcion = models.CharField(
        max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = 'Especialidades'


class Profesional(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    especialidad = models.ManyToManyField(Especialidad)
    numero_prestador = models.IntegerField(null=True, blank=True)
    numero_prestador_vencimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=12, blank=False, null=False)
    telefono_opcional = models.CharField(max_length=12, null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.usuario.last_name) + ', ' + str(self.usuario.first_name)

    class Meta:
        verbose_name_plural = 'Profesionales'


# Create your models here.
