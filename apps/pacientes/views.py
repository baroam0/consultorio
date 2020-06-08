
import ast
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
                return redirect('/pacienteeditar/' + str(consulta.pk))
            else:
                return render(
                    request,
                    'pacientes/paciente_edit.html',
                    {
                        "form": form,
                    })
    else:
        form = PacienteForm()
        return render(
            request,
            'pacientes/paciente_edit.html',
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
        form_obrasocial = PacienteObraSocialForm()
        tiene_obrasocial = verifica_obrasocial(consulta)
        if tiene_obrasocial == False:
            mensaje = "ESTE PACIENTE NO POSEE OBRA SOCIAL REGISTRADA"
            return render(
                request,
                'pacientes/paciente_edit.html',
                {
                    "form": form,
                    "form_obrasocial": form_obrasocial,
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


def ajaxpacienteobrasocialnuevo(request):
    parametro = request.GET.get('term')

    consulta = ObraSocial.objects.filter(
        Q(descripcion__icontains=parametro) |
        Q(abreviatura__icontains=parametro)
    )

    dict_tmp = dict()
    list_tmp = list()

    if len(consulta) > 0:
        for i in consulta:
            dict_tmp["id"] = i.pk
            dict_tmp["text"] = i.descripcion.upper()
            list_tmp.append(dict_tmp)
            dict_tmp = dict()

    return JsonResponse(list_tmp, safe=False)


@csrf_exempt
def ajax_grabarpacienteobrasocialnuevo(request):
    datos = ast.literal_eval(request.POST["datos"]) 
    paciente = Paciente.objects.get(pk=datos["paciente"])
    obraosocial = ObraSocial.objects.get(pk=int(datos["obrasocial"]))
    paciente_obrasocial = PacienteObraSocial(
        paciente = paciente,
        obrasocial = obraosocial,
        numeroafiliado = datos["numeroafiliado"],
        observaciones = datos["observaciones"],
    )
    paciente_obrasocial.save()
    
    #consulta = PacienteObraSocial.objects.filter(paciente=paciente).select_related('obrasocial')
    consulta = PacienteObraSocial.objects.filter(paciente=paciente)

    print("*******************************************")
    for i in consulta:
        print(i.pk)
        print(i.obrasocial)
        print(i.numeroafiliado)
        print(i.observaciones)
    
    dict_tmp = dict()
    list_tmp = list()

    if len(consulta) > 0:
        for i in consulta:
            dict_tmp["id_obrasocial"] = i.pk
            dict_tmp["descripcion"] = i.obrasocial.descripcion
            dict_tmp["numeroafiliado"] = i.numeroafiliado
            dict_tmp["observaciones"] = i.observaciones
            list_tmp.append(dict_tmp)
            dict_tmp = dict()

    return JsonResponse(list_tmp, safe=False)

    

# Create your views here.
