
from django.contrib import admin

from .models import Alumno, Curso, Modalidad, Modulo, Profesion

admin.site.register(Alumno)
admin.site.register(Curso)
admin.site.register(Modalidad)
admin.site.register(Modulo)
admin.site.register(Profesion)


# Register your models here.
