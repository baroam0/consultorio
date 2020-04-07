
from django.db import models


class ObraSocial(models.Model):
    descripcion = models.CharField(max_length=200, null=False, blank=False, unique=True)
    abreviatura = models.CharField(max_length=50, null=False, blank=False, unique=False)
    telefono = models.CharField(max_length=20, blank=False, null=False)
    telefono_opcional = models.CharField(max_length=12, null=True, blank=True)
    correo_electronico = models.EmailField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.descripcion.upper() + ' - ' +  self.abreviatura.upper()

    class Meta:
        verbose_name_plural = 'Obras Sociales'


class Prestacion(models.Model):
    codigo = models.CharField(max_length=30, blank=True, null=True)
    descripcion = models.CharField(max_length=40, blank=True, null=True)
    
    def __str__(self):
        return self.codigo + ' - ' + self.descripcion

    class Meta:
        verbose_name_plural = "Prestaciones" 


class Nucleador(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion.upper()
    
    class Meta:
        verbose_name_plural = "Nucleadores"


class NucleadorPrestacion(models.Model):
    nucleador = models.ForeignKey(
        Nucleador, on_delete=models.CASCADE, default=1)
    obrasocial = models.ForeignKey(ObraSocial, on_delete=models.CASCADE)
    prestacion = models.ForeignKey(Prestacion, on_delete=models.CASCADE)
    importe = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.prestacion) + '-' + str(self.importe)
    
    class Meta:
        verbose_name_plural = "Nucleadores Prestaciones"

# Create your models here.
