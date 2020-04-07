from django.contrib import admin

from .models import Banco, TipoCuenta, DatosBancarios

admin.site.register(Banco)
admin.site.register(TipoCuenta)
admin.site.register(DatosBancarios)

# Register your models here.
