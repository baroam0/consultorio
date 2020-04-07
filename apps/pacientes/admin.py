from django.contrib import admin

from .models import TipoDocumento, Paciente, PacienteObraSocial

admin.site.register(TipoDocumento)
admin.site.register(Paciente)
admin.site.register(PacienteObraSocial)

# Register your models here.
