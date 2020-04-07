from django.db import models


class Catalogo(models.Model):
    clave = models.CharField(max_length=20, null=True, blank=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.clave + '-' + self.descripcion
    
    class Meta:
        verbose_name_plural = "CIE10s"

# Create your models here.
