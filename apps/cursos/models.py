
from django.db import models


class Alumno(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Alumnos"    


class Curso(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Cursos"


class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField()

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Modulos"
        

# Create your models here.
