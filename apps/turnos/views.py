
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
    obras_sociales = ObraSocial.objects.all().order_by("abreviatura")

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
                'obrassociales': obras_sociales,
                'pacientes': pacientes,
                'profesionales': profesionales,
                'resultados': resultados
            }
        )


def nuevoturno(request):
    if request.POST:
        form = TurnoForm(request.POST)

        fechahora = request.POST["fechahora"]

        if len(fechahora) > 17:
            fechahora = datetime.strptime(fechahora, "%d/%m/%Y %H:%M:%S")
        else:
            fechahora = datetime.strptime(fechahora, "%d/%m/%Y %H:%M")

        paciente = request.POST["paciente"]
        profesional = request.POST["profesional"]

        try:
            consulta = Turno.objects.get(fechahora=fechahora, profesional=profesional)
        except:
            consulta = None

        if not consulta:
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "SE HAN GUARDADO EL TURNO ")
                return redirect('/turnolistado/')
            else:
                return render(
                    request,
                    'turnos/turno_edit.html',
                    {
                        "form": form,
                    })
        else:
            messages.error(
                request,
                "YA EXISTE UN TURNO EN ESE HORARIO PARA ESE PACIENTE Y ESE PROFESIONAL"
            )
            return render(
                request,
                'turnos/turno_edit.html',
                {
                    "form": form,
                }
            )
    else:
        form = TurnoForm()
        return render(
            request,
            'turnos/turno_edit.html',
            {
                "form": form,
            }
        )


def editarturno(request, pk):
    turno = Turno.objects.get(pk=pk)

    if request.POST:
        fechahora = request.POST["fechahora"]

        if len(fechahora) > 17:
            fechahora = datetime.strptime(fechahora, "%d/%m/%Y %H:%M:%S")
        else:
            fechahora = datetime.strptime(fechahora, "%d/%m/%Y %H:%M")
        paciente = request.POST["paciente"]
        profesional = request.POST["profesional"]

        try:
            consulta = Turno.objects.get(
                fechahora=fechahora,
                profesional=profesional
            )
        except:
            consulta = None

        if not consulta:
            form = TurnoForm(request.POST, instance=turno)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    "SE HAN GUARDADO EL TURNO ")
                return redirect('/turnolistado/')
            else:
                return render(
                    request,
                    'turnos/turno_edit.html',
                    {
                        "form": form,
                    })
        else:
            form = TurnoForm(instance=turno)
            messages.error(
                request,
                "YA EXISTE UN TURNO EN ESE HORARIO PARA ESE PACIENTE Y ESE PROFESIONAL"
            )
            return render(
                request,
                'turnos/turno_edit.html',
                {
                    "form": form,
                }
            )
    else:
        form = TurnoForm(instance=turno)
        return render(
            request,
            'turnos/turno_edit.html',
            {
                "form": form,
            }
        )


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


def ajax_grabarturno(request):
    fecha = datetime.today()

    vectormateriales=request.POST.getlist('vectormateriales[]')
    vectorcantidades=request.POST.getlist('vectorcantidades[]')
    vectorunidades=request.POST.getlist('vectorunidades[]')
    vectorprecios=request.POST.getlist('vectorprecios[]')

    vectormateriales, vectorcantidades, vectorcantidades

    operacion = Operacion(
        fecha=fecha
    )

    operacion.save()
    operacion = Operacion.objects.latest("pk")

    for (material, unidad, cantidad, precio) in zip(vectormateriales, vectorunidades, vectorcantidades, vectorprecios):
        material = Material.objects.get(pk=int(material))

        detalleoperacion = DetalleOperacion(
            operacion=operacion,
            material=material,
            cantidad=cantidad,
            precio_unitario=precio,
            precio_subtotal= float(cantidad)*float(precio)
        )

        detalleoperacion.save()

    data = {
        "status": 200
    }
    return JsonResponse(data)


# Create your views here.
