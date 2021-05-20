
from datetime import datetime
import json
import pytz

from django.contrib import messages
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.timezone import localtime

from apps.obrassociales.models import ObraSocial
from apps.pacientes.models import Paciente
from apps.profesionales.models import Profesional
from apps.turnos.forms import TurnoForm
from apps.turnos.models import Turno


def validaturno(fecha_hora,paciente,profesional):
    
    try:
        consulta = Turno.objects.get(
            fechahora = fecha_hora,
            paciente = paciente,
            profesional = profesional
        )
        return 1
    except:
        return 0


def listadoturno(request):
    """
    Funcion mostrar solamente el calendario y los turnos de un solo profesional
    """
    obrassociales = ObraSocial.objects.all()
    profesionales = Profesional.objects.all()
    pacientes = Paciente.objects.all()
    obras_sociales = ObraSocial.objects.all().order_by("abreviatura")

    if "select_profesional_busqueda" in request.GET:
        if int(request.GET.get("select_profesional_busqueda")) == 0:
            resultados = Turno.objects.all()
        else:
            profesional = Profesional.objects.get(pk=request.GET.get("select_profesional_busqueda"))
            resultados = Turno.objects.filter(profesional=profesional)
        for f in resultados:
            print(f.fechahora)
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
                'obrassociales': obras_sociales,
                'pacientes': pacientes,
                'profesionales': profesionales,
                'resultados': resultados
            }
        )

@csrf_exempt
def nuevoturno(request):
    profesional = request.POST["profesional_id"]
    paciente = request.POST["paciente_id"]
    fecha = request.POST["fecha"]
    hora = request.POST["hora"]
    obrasocial = request.POST["obrasocial"]
    asistio = request.POST["asistio"]
    entrega = request.POST["entrega"]
    entregaparcial = request.POST["entregaparcial"]
    observacion = request.POST["observacion"]

    fecha_hora = str(fecha) + " " + str(hora)

    fecha_hora_obj = datetime.strptime(fecha_hora, '%d/%m/%Y %H:%M')

    obrasocial = ObraSocial.objects.get(pk=obrasocial)
    paciente = Paciente.objects.get(pk=paciente)
    profesional = Profesional.objects.get(pk=profesional)

    if asistio == "false":
        asistio = False
    else:
        asistio = True
    
    if entrega == "false":
        entrega = False
    else:
        entrega = True
    
    if entregaparcial == "false":
        entregaparcial = False
    else:
        entregaparcial = True
    
    valor = validaturno(fecha_hora_obj,paciente,profesional)

    if valor == 0:
        turno = Turno(
            fechahora = fecha_hora_obj,
            paciente = paciente,
            obrasocial = obrasocial,
            profesional = profesional,
            asistio = asistio,
            entrega = entrega,
            entrega_parcial = entregaparcial,
            observacion = observacion
        )
        turno.save()
        data = {
            "status": 200,
            "mensaje": "El turno se ha guardado"
        }
    else:
        data = {
            "status": 400,
            "mensaje": "El Turno no esta disponible"
        }

    return JsonResponse(data)


def cargaturnomodal(request,pk):

    """
    
    deals_utc = Deal.objects.filter(id=62).values("created_at")
    deals_local = {"created_at": localtime(dt, tz) for dt in deals_utc.values()}
    """
    tz = pytz.timezone('America/Argentina/Buenos_Aires')

    turno = Turno.objects.select_related('paciente').select_related('obrasocial').get(pk=pk)

    print("****************************************")
    #fechahora_parseada = turno.fechahora.strftime('%d/%m/%Y %H:%M')
    #fechahora_parseada = localtime(turno.fechahora.strftime('%d/%m/%Y %H:%M'),tz) 
    fechahora_parseada = localtime(turno.fechahora)

    print(fechahora_parseada.strftime('%H:%M'))
    print("---------------------------------------")

    data = {
        "turno_id": turno.pk,
        "paciente_id": turno.paciente.id,
        "paciente": str(turno.paciente.apellido) + "," + str(turno.paciente.nombre),
        "fecha": fechahora_parseada.strftime('%d/%m/%Y'),
        "hora": fechahora_parseada.strftime('%H:%M'),
        "obrasocial_id": turno.obrasocial.pk,
        "obrasocial": turno.obrasocial.descripcion,
        "obrasocial_abreviatura": turno.obrasocial.abreviatura,
        "asistio": turno.asistio,
        "entrega": turno.entrega,
        "entrega_parcial": turno.entrega_parcial,
        "observacion": turno.observacion
    }

    return JsonResponse(data, safe=False)

def ajax_editarturno(request, pk):
    return None


def editarturno(request, pk):
    return None


# Create your views here.
