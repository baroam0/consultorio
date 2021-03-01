
from datetime import datetime
from django.db import models

from apps.catalogosenfermedades.models import Catalogo
from apps.obrassociales.models import ObraSocial
from apps.profesionales.models import Profesional


class TipoDocumento(models.Model):
    descripcion = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.descripcion.upper()
    
    class Meta:
        verbose_name_plural = "Tipos de Documentos"


class Paciente(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido = models.CharField(max_length=50, null=False, blank=False)
    tipodocumento = models.ForeignKey(
        TipoDocumento,
        on_delete=models.CASCADE, 
        default=1)
    numero_documento = models.CharField(max_length=15, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=12, blank=False, null=False)
    telefono_opcional = models.CharField(max_length=12, null=True, blank=True)
    correo_electronico = models.EmailField(null=True, blank=True)
    domicilio = models.CharField(max_length=200, null=True, blank=True)
    ocupacion = models.CharField(max_length=50, null=True, blank=True)
    fecha_admision = models.DateField(null=True, blank=True)
    profesional_tratante = models.ForeignKey(
        Profesional,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    medicacion = models.CharField(max_length=200, null=True, blank=True)
    fue_al_psicologo = models.CharField(max_length=200, null=True, blank=True)
    grupo_familiar = models.CharField(max_length=200, null=True, blank=True)
    diagnostico = models.ForeignKey(
        Catalogo, on_delete=models.CASCADE, null=True, blank=True
    )
    observacion = models.TextField(null=True, blank=True)

    def get_edad(self):
        hoy = datetime.today().date()
        #fechanac = datetime.strptime(fechanac, "%Y-%m-%d")
        anios = int((hoy - self.fecha_nacimiento).days/365.25)
        return anios

    def __str__(self):
        return self.apellido.upper() + ', ' +  self.nombre.upper()

    class Meta:
        verbose_name_plural = 'Pacientes'


class PacienteObraSocial(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, default=1)
    obrasocial = models.ForeignKey(ObraSocial, on_delete=models.CASCADE)
    numeroafiliado = models.CharField(max_length=20, null=True, blank=True)
    observaciones = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.paciente) + '-' + str(self.obrasocial) + '-' + self.numeroafiliado 

    class Meta:
        verbose_name_plural = "Pacientes - Obras Sociales"


# Create your models here.
