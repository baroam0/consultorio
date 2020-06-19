
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from apps.profesionales.models import Profesional
from apps.turnos.forms import TurnoForm
from apps.turnos.models import Turno


def listadoturno(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username))
        if not usuario.is_staff:
            usuarioprofesional = Profesional.objects.get(usuario=usuario)

    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")

        if parametro == "" or None:
            if usuario.is_staff:
                consulta = Turno.objects.filter(
                    fechahora__date=datetime.today(),
                    asistio=False
                ).order_by('fechahora')
            
                paginador = Paginator(consulta, 20)
                page = 1
                resultados = paginador.get_page(page)

                return render(
                    request,
                    'turnos/turno_list.html',
                    {
                        'resultados': resultados,
                    }
                )

        if "/" in parametro:
            parametro = datetime.strptime(parametro, "%d/%m/%Y")

            if usuario.is_staff:
                consulta = Turno.objects.filter(
                    fechahora__year=parametro.year,
                    fechahora__month=parametro.month,
                    fechahora__day=parametro.day,
                    asistio=False,
                )
            else:
                consulta = Turno.objects.filter(
                    fechahora__year=parametro.year,
                    fechahora__month=parametro.month,
                    fechahora__day=parametro.day,
                    profesional=usuarioprofesional,
                    asistio=False
                )
            return render(
                request,
                'turnos/turno_list.html',
                {
                    'resultados': consulta,
                }
            )

        if "-" in parametro:
            parametro = datetime.strptime(parametro, "%d-%m-%Y")
            if usuario.is_staff:
                consulta = Turno.objects.filter(
                    fechahora__year=parametro.year,
                    fechahora__month=parametro.month,
                    fechahora__day=parametro.day,
                    asistio=False,
                )
            else:
                consulta = Turno.objects.filter(
                    fechahora__year=parametro.year,
                    fechahora__month=parametro.month,
                    fechahora__day=parametro.day,
                    profesional=usuarioprofesional,
                    asistio=False
                )
            
            return render(
                request,
                'turnos/turno_list.html',
                {
                    'resultados': consulta,
                }
            )

        if usuario.is_staff:
            consulta = Turno.objects.filter(
                Q(paciente__nombre__icontains=parametro) |
                Q(paciente__apellido__icontains=parametro)
            ).order_by('fechahora')
        else:
            consulta = Turno.objects.filter(
                profesional=usuarioprofesional,
                asistio=False)
    else:
        if usuario.is_staff:
            consulta = Turno.objects.filter(
                fechahora__date=datetime.today(),
                asistio=False,
            ).order_by('fechahora')
        else:
            consulta = Turno.objects.filter(
                fechahora__date=datetime.today(),
                profesional=usuarioprofesional,
                asistio=False
            ).order_by('fechahora')

    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    
    return render(
        request,
        'turnos/turno_list.html',
        {
            'resultados': resultados,
        }
    )
    

def nuevoturno(request):
    if request.POST:
        form = TurnoForm(request.POST)

        fechahora = request.POST["fechahora"]
        paciente = request.POST["paciente"]
        profesional = request.POST["profesional"]

        fechahora = datetime.strptime(fechahora, "%d/%m/%Y %H:%M")

        try:
            consulta = Turno.objects.get(fechahora=fechahora, paciente=paciente, profesional=profesional)
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
        fechahora = datetime.strptime(fechahora, "%d/%m/%Y %H:%M")
        paciente = request.POST["paciente"]
        profesional = request.POST["profesional"]

        try:
            consulta = Turno.objects.get(
                fechahora=fechahora,
                paciente=paciente,
                profesional=profesional
            )
        except:
            consulta = None

        if not consulta:
            form = TurnoForm(request.POST, instance=consulta)
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




# Create your views here.
