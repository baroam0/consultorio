
from datetime import datetime

import pytz

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils.timezone import localtime

from apps.obrassociales.models import ObraSocial
from apps.pacientes.models import Paciente
from apps.profesionales.models import Profesional
from apps.turnos.models import Turno


def validaturno(fecha_hora,paciente,profesional):
    try:
        consulta = Turno.objects.get(
            fechahora = fecha_hora,
            profesional = profesional
        )
        return 1
    except:
        return 0


def validaturnoedicion(turno_id,fecha_hora,paciente,profesional):
    
    consulta = Turno.objects.filter(
        fechahora = fecha_hora,
        profesional = profesional
    ).exclude(pk=turno_id)
    if consulta:
        return 1
    else:
        return 0


@csrf_exempt
def borrarturno(request, pk):
    turno_id = request.POST['turno_id']
    turno = Turno.objects.get(pk=int(turno_id))
    turno.delete()
    data = {
        "status": 200
    }

    return data


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
            #resultados = Turno.objects.all()
            resultados = Turno.objects.none()
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
    tz = pytz.timezone('America/Argentina/Buenos_Aires')
    turno = Turno.objects.select_related('paciente').select_related('obrasocial').select_related('profesional').get(pk=pk)
    fechahora_parseada = localtime(turno.fechahora)

    data = {
        "turno_id": turno.pk,
        "paciente_id": turno.paciente.id,
        "paciente": str(turno.paciente.apellido) + "," + str(turno.paciente.nombre),
        "profesional_id": turno.profesional.pk,
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



@csrf_exempt
def editarturno(request, pk):
    turno = Turno.objects.get(pk=pk)

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

    valor = validaturnoedicion(turno.pk,fecha_hora_obj,paciente,profesional)

    print(valor)

    if valor == 0:
        turno.fechahora = fecha_hora_obj
        turno.paciente = paciente
        turno.profesional = profesional
        turno.obrasocial = obrasocial
        turno.asistio = asistio
        turno.entrega = entrega
        turno.entrega_parcial = entregaparcial
        turno.observacion = observacion
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


# Create your views here.
