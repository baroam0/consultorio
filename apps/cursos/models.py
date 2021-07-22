
from django.db import models

from apps.pacientes.models import TipoDocumento

class Profesion(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Profesiones"


class Alumno(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    tipodocumento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    numerodocumento = models.IntegerField(null=False, blank=False)
    matricula = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.apellido + "," + self.nombre
    
    class Meta:
        verbose_name_plural = "Alumnos"


class Curso(models.Model):
    descripcion = models.CharField(max_length=100, null=False, blank=False, unique=True)
    dureacion = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Cursos"


class Modulo(models.Model):
    descripcion = models.CharField(max_length=100, null=False, blank=False, unique=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Cursos"


# Create your models here.
