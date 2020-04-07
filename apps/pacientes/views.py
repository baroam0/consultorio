
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import PacienteForm, PacienteObraSocialForm
from .models import Paciente, PacienteObraSocial
from apps.helpers.edad import edad
from apps.obrassociales.models import ObraSocial
from apps.pacientes.models import TipoDocumento
from apps.profesionales.models import Profesional

from .helpers import verifica_paciente, verifica_obrasocial


def listadopaciente(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username))
        if not usuario.is_staff:
            usuarioprofesional = Profesional.objects.get(usuario=usuario)

    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")        
        if usuario.is_staff:
            consulta = Paciente.objects.filter(
                Q(apellido__icontains=parametro) |
                Q(nombre__contains=parametro)
            )
        else:
            consulta = Paciente.objects.filter(
                Q(apellido__icontains=parametro) |
                Q(nombre__contains=parametro)
            ).filter(profesional_tratante=usuarioprofesional)
            #consulta = consulta.filter(profesional_tratante=usuarioprofesional)
            
    else:
        if usuario.is_staff:
            consulta = Paciente.objects.all()
        else:
            consulta = Paciente.objects.filter(profesional_tratante=usuarioprofesional)

    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'pacientes/paciente_list.html', {'resultados': resultados})


def nuevopaciente(request):
    if request.POST:
        form = PacienteForm(request.POST)

        existe = verifica_paciente(request.POST['numero_documento'])

        if existe == True:
            messages.success(request, "EL PACIENTE YA EXISTE EN LOS REGISTROS")
            return redirect('/pacientelistado')
        else:
            if form.is_valid():
                form.save()
                consulta = Paciente.objects.latest('pk')
                messages.success(
                    request,
                    "SE HAN GUARDADO LOS DATOS DEL PACIENTE " + str(consulta.apellido).upper() + ', ' + str(consulta.nombre).upper())
                return redirect('/pacienteobrasocialnuevo')
            else:
                return render(
                    request,
                    'pacientes/paciente_nuevo.html',
                    {
                        "form": form,
                    })
    else:
        form = PacienteForm()
        return render(
            request,
            'pacientes/paciente_nuevo.html',
            {
                "form": form,
            }
        )


def editarpaciente(request, pk):
    consulta = Paciente.objects.get(pk=pk)
    anios = edad(consulta.fecha_nacimiento)
    if request.POST:
        form = PacienteForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA MOFICICADO EL PACIENTE")
            return redirect('/pacientelistado')
        else:
            return render(request, "pacientes/paciente_edit.html", {"form": form})
    else:
        form = PacienteForm(instance=consulta)
        tiene_obrasocial = verifica_obrasocial(consulta)
        if tiene_obrasocial == False:
            mensaje = "ESTE PACIENTE NO POSEE OBRA SOCIAL REGISTRADA"
            return render(
                request,
                'pacientes/paciente_edit.html',
                {
                    "form": form,
                    "mensaje": mensaje,
                    "anios": anios,
                    "paciente": consulta.pk,
                }
            )
        else:
            obrassociales = PacienteObraSocial.objects.filter(
                paciente = consulta
            )
            return render(
                request,
                'pacientes/paciente_edit.html',
                {
                    "form": form,
                    "obrassociales": obrassociales,
                    "anios": anios
                }
            )


def listadopacienteobrasocial(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")

        if parametro.isnumeric():
            consulta = PacienteObraSocial.objects.filter(
                numeroafiliado__contains=parametro
            )
        else:
            consulta = PacienteObraSocial.objects.filter(
                Q(paciente__apellido__contains=parametro) | 
                Q(paciente__nombre__contains=parametro)
            )
    else:
        consulta = PacienteObraSocial.objects.all()
    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'pacientes/pacienteobrasocial_list.html', {'resultados': resultados})


def nuevopacienteobrasocial(request,):
    
    if request.POST:
        form = PacienteObraSocialForm(request.POST)
        if form.is_valid():
            pacienteobrasocial = form.save()
            pacienteobrasocial.save()
            messages.success(request, "SE HAN GUARDADO LOS DATOS")
            return redirect('/pacientelistado')
        else:
            return render(
                request,
                'pacientes/pacienteobrasocial_nuevo.html',
                {"form": form,})
    else:
        form = PacienteObraSocialForm()
        return render(request, 'pacientes/pacienteobrasocial_edit.html', {"form": form})


def editarpacienteobrasocial(request, pk):
    consulta = PacienteObraSocial.objects.get(pk=pk)

    if request.POST:
        form = PacienteObraSocialForm(request.POST, instance=consulta)
        if form.is_valid():
            pacienteobrasocial = form.save()
            pacienteobrasocial.save()
            messages.success(request, "SE HA MOFICICADO LOS DATOS")
            return redirect('/pacienteobrasociallistado')
        else:
            return render(request, "pacientes/pacienteobrasocial_edit.html", {"form": form})
    else:
        form = PacienteObraSocialForm(instance=consulta)
        return render(request, 'pacientes/pacienteobrasocial_edit.html', {"form": form})

# Create your views here.
