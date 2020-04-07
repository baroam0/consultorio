from django.contrib import admin

from .models import ObraSocial, Prestacion, Nucleador, NucleadorPrestacion

admin.site.register(ObraSocial)
admin.site.register(Prestacion)
admin.site.register(Nucleador)
admin.site.register(NucleadorPrestacion)

# Register your models here.
