
from datetime import datetime
from django.db import models

from apps.pacientes.models import TipoDocumento


class Profesion(models.Model):
    """Clase para representar Profesion """
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Profesiones"


class Alumno(models.Model):
    """Clase para representar Alumno"""
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    numerodocumento = models.IntegerField(null=False, blank=False)
    matricula = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.apellido + "," + self.nombre

    class Meta:
        verbose_name_plural = "Alumnos"


class Modalidad(models.Model):
    """Clase para representar Modalidad"""
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion.upper()

    class Meta:
        verbose_name_plural = "Modalidades"


class Curso(models.Model):
    """Clase para representar el Curso"""
    descripcion = models.CharField(
        max_length=100, null=False, blank=False, unique=True)
    duracion = models.CharField(max_length=100, null=True, blank=True)
    presencial = models.BooleanField(default=False)
    virtual = models.BooleanField(default=False)

    def __str__(self):
        return self.descripcion.upper()

    def save(self, *args, **kwargs):
        if self.pk is None:
            hoy = datetime.today()
            #hoy_str = hoy.strftime("%d-%m-%Y")
            hoy_str = hoy.strftime("%Y-%m-%d")
            self.descripcion = str(self.descripcion) + "_" + str(hoy_str)
            super(Curso, self).save(*args, **kwargs)
        else:
            super(Curso, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Cursos"


class Modulo(models.Model):
    """Clase para representar el modulo"""
    descripcion = models.CharField(
        max_length=100, null=False, blank=False, unique=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    valor = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return self.descripcion.title()

    class Meta:
        verbose_name_plural = "Modulos"




# Create your models here.
