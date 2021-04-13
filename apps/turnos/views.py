
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from apps.obrassociales.models import ObraSocial
from apps.pacientes.models import Paciente
from apps.profesionales.models import Profesional
from apps.turnos.forms import TurnoForm
from apps.turnos.models import Turno


def listadoturno(request):
    """
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username))
        if not usuario.is_staff:
            usuarioprofesional = Profesional.objects.get(usuario=usuario)
        else:
            profesionales = Profesional.objects.all()
    """
    obrassociales = ObraSocial.objects.all()
    profesionales = Profesional.objects.all()
    pacientes = Paciente.objects.all()

    if "select_profesional_busqueda" in request.GET:
        if int(request.GET.get("select_profesional_busqueda")) == 0:
            resultados = Turno.objects.all()
        else:
            profesional = Profesional.objects.get(pk=request.GET.get("select_profesional_busqueda"))
            resultados = Turno.objects.filter(profesional=profesional)
        return render(
            request,
            'turnos/turno_list.html',
            {
                'obrassociales': obrassociales,
                'pacientes': pacientes,
                'profesionales': profesionales,
                'resultados': resultados
            }
        )
    else:
        resultados = None
        return render(
            request,
            'turnos/turno_list.html',
            {
                'obrassociales': obrassociales,
                'pacientes': pacientes,
                'profesionales': profesionales,
                'resultados': resultados
            }
        )


def ajax_nuevoturno(request):
    return None

def ajax_editarturno(request, pk):
    return None

def ajax_asistiopaciente(request):
    parametro = request.GET.get("parametro")
    consulta = Turno.objects.get(pk=parametro)
    consulta.asistio = True
    consulta.save()
    dicc_tmp = dict()
    dicc_tmp["response"] = 200
    return JsonResponse(dicc_tmp, safe=False)


def ajax_turnoborrar(request):
    parametro = request.GET.get("parametro")
    consulta = Turno.objects.get(pk=parametro)
    consulta.delete()
    dicc_tmp = dict()
    dicc_tmp["response"] = 200
    return JsonResponse(dicc_tmp, safe=False)




# Create your views here.
