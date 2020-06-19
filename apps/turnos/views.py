
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from apps.profesionales.models import Profesional
from apps.turnos.forms import TurnoForm
from apps.turnos.models import Turno


def listadoturno(request):

    profesionales = Profesional.objects.all().order_by('usuario__last_name')
    
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username))
        if not usuario.is_staff:
            usuarioprofesional = Profesional.objects.get(usuario=usuario)

    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if usuario.is_staff:
            consulta = Turno.objects.filter(
                Q(paciente__nombre__icontains=parametro) |
                Q(paciente__apellido__icontains=parametro)
            ).order_by('fechahora')
        else:
            consulta = Turno.objects.filter(profesional=usuarioprofesional)
    else:
        if usuario.is_staff:
            consulta = Turno.objects.filter(
                fechahora__date=datetime.now()
            ).order_by('fechahora')
        else:
            consulta = Turno.objects.filter(
                fechahora__date=datetime.today(),
                profesional=usuarioprofesional
            ).order_by('fechahora')

    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    if usuario.is_staff:
        return render(
            request,
            'turnos/turno_list.html',
            {
                'resultados': resultados,
                'profesionales': profesionales
            }
        )
    else:
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
        form = TurnoForm(instance=consulta)
        return render(
            request,
            'turnos/turno_edit.html',
            {
                "form": form,
            }
        )


# Create your views here.
