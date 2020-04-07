
from django.contrib.auth.models import User
from django.db import models


class Titular(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.get_full_name().upper()


class Banco(models.Model):
    descripcion = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Bancos"


class TipoCuenta(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)
    abreviatura = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Tipos de Cuentas"


class DatosBancarios(models.Model):
    titular = models.ForeignKey(Titular, on_delete=models.CASCADE)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    tipocuenta = models.ForeignKey(TipoCuenta, on_delete=models.CASCADE)
    cbu = models.CharField(max_length=22, null=False, blank=False)

    def __str__(self):
        return str(self.banco) + ' - ' + str(self.tipocuenta) + ' - ' + self.cbu

    class Meta:
        verbose_name_plural = "Datos Bancarios"

# Create your models here.
