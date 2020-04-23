"""consultorio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import home, loginusuario, salir

from apps.bancos.views import listadodatosbancarios, nuevodatobancario, editardatobancario

from apps.catalogosenfermedades.views import ajaxcatalogo

from apps.obrassociales.views import editarobrasocial, nuevaobrasocial, \
    obrasociallistado, prestacionlistado, nuevaprestacion, editarprestacion, \
    nucleadorprestacionlistado, nuevonucleadorprestacion, \
    editarnucleadorprestacion, ajaxobrasocial

from apps.pacientes.views import listadopaciente, nuevopaciente, \
    editarpaciente, listadopacienteobrasocial, nuevopacienteobrasocial, \
    editarpacienteobrasocial

from apps.profesionales.views import listadoprofesional, \
    editarprofesional, perfil, crearprofesional

"""
from apps.turnos.views import turnoasistencia, turnolistado, turnonuevo, \
    turnoborrar, turnoeditar
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('login/', loginusuario),
    path('salir/', salir),
    path('ajaxobrasocial/', ajaxobrasocial),
    path('ajaxcatalogo/', ajaxcatalogo),
    path('datosbancarioslistado/', listadodatosbancarios),
    path('datobancarionuevo/', nuevodatobancario),
    path('datobancarioeditar/<int:pk>/', editardatobancario),
    path('nucleadorprestacionlistado/', nucleadorprestacionlistado),
    path('nucleadorprestacionnuevo/', nuevonucleadorprestacion),
    path('nucleadorprestacioneditar/<int:pk>/', editarnucleadorprestacion),
    path('obrasociallistado/', obrasociallistado),
    path('obrasocialnuevo/', nuevaobrasocial),
    path('obrasocialeditar/<int:pk>/', editarobrasocial),
    path('prestacionlistado/', prestacionlistado),
    path('prestacionnueva/', nuevaprestacion),
    path('prestacioneditar/<int:pk>/', editarprestacion),
    path('pacientelistado/', listadopaciente),
    path('pacientenuevo/', nuevopaciente),
    path('pacienteeditar/<int:pk>/', editarpaciente),
    path('pacienteobrasociallistado/', listadopacienteobrasocial),
    path('pacienteobrasocialnuevo/', nuevopacienteobrasocial),
    path('pacienteobrasocialeditar/<int:pk>/', editarpacienteobrasocial),
    path('profesionallistado/', listadoprofesional),
    path('profesionalnuevo/', crearprofesional),
    path('perfil/', perfil),
    path('profesionaleditar/<int:pk>/', editarprofesional),
    #path('turnoasistencia/', turnoasistencia),
    #path('turnolistado/', turnolistado),
    #path('turnonuevo/', turnonuevo),
    #path('turnoborrar/', turnoborrar),
    #path('turnoeditar/<int:pk>/', turnoeditar),
]
