
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
    
    if "selectProfesional" in request.GET:
        parametro_profesional = request.GET.get("selectProfesional")
        if parametro_profesional == "0" or parametro_profesional == "" or parametro_profesional == None:
            #parametro_profesional = None
            profesional = Profesional.objects.none()
        else: 
            profesional = Profesional.objects.get(pk=int(parametro_profesional))
    else:
        profesional = Profesional.objects.none()

    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if usuario.is_staff:
            if parametro == "":
                print("********************************************************************")
                if not profesional:
                    consulta = Paciente.objects.all().order_by('apellido')
                else:
                    consulta = Paciente.objects.filter(
                        profesional_tratante=profesional
                    ).order_by('apellido')
            else:
                
                consulta = Paciente.objects.filter(
                    Q(apellido__icontains=parametro) |
                    Q(nombre__contains=parametro) |
                    Q(ocupacion__contains=parametro)
                ).order_by('apellido')
        else:
            if parametro == "":
                consulta = Paciente.objects.filter(
                    profesional_tratante=usuarioprofesional).order_by('apellido')
            else:
                consulta = Paciente.objects.filter(
                    Q(apellido__icontains=parametro) |
                    Q(nombre__contains=parametro) |
                    Q(ocupacion__contains=parametro)
                ).filter(profesional_tratante=usuarioprofesional).order_by('apellido')
    else:
        parametro = ""
        if usuario.is_staff:
            if profesional:
                consulta = Paciente.objects.filter(profesional_tratante=profesional).order_by('apellido')
            else:
                consulta = Paciente.objects.all().order_by('apellido')
        else:
            consulta = Paciente.objects.filter(profesional_tratante=usuarioprofesional).order_by('apellido')

    paginador = Paginator(consulta, 20)

    print(paginador)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    
    resultados = paginador.get_page(page)

    profesionales = Profesional.objects.all()

    if parametro != "":
        return render(request, 'pacientes/paciente_list.html', {'resultados': resultados, 'parametro': parametro, 'profesionales': profesionales})
    else:
        return render(request, 'pacientes/paciente_list.html', {'resultados': resultados, 'profesionales': profesionales})


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
            paciente_obrassociales = PacienteObraSocial.objects.filter(
                paciente = consulta
            )
            return render(
                request,
                'pacientes/paciente_edit.html',
                {
                    "form": form,
                    "paciente_obrassociales": paciente_obrassociales,
                    "form_obrasocial": form_obrasocial,
                    "anios": anios
                }
            )


def ajax_obrasocial_paciente(request, pk):
    paciente  = Paciente.objects.get(pk=pk)

    pacientes_obrasociales = PacienteObraSocial.objects.filter(
        paciente=paciente
    )

    dict_tmp = dict()
    list_tmp = list()

    if pacientes_obrasociales:
        for dato in pacientes_obrasociales:
            dict_tmp["id_obrasocial"] = dato.obrasocial.pk
            dict_tmp["descripcion_obrasocial"] = dato.obrasocial.descripcion.upper()
            dict_tmp["abreviatura_obrasocial"] = dato.obrasocial.abreviatura.upper()
            list_tmp.append(dict_tmp)
            dict_tmp = dict()
    else:
        pacientes_obrasociales = None

    return JsonResponse(list_tmp, safe=False)


def ajax_profesionaltratante_paciente(request, pk):
    paciente  = Paciente.objects.get(pk=pk)
    profesional = Profesional.objects.get(pk=paciente.profesional_tratante.pk)
    nombre_profesional = str(profesional.usuario.first_name) + ', ' + str(profesional.usuario.last_name)

    dict_tmp = dict()
    list_tmp = list()

    if paciente:
        dict_tmp["id_profesional"] = profesional.pk
        dict_tmp["profesional"] = nombre_profesional.upper()
        list_tmp.append(dict_tmp)
    else:
        paciente = None

    return JsonResponse(list_tmp, safe=False)


@csrf_exempt
def ajax_nuevopacienteobrasocial(request):
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
    
    consulta = PacienteObraSocial.objects.filter(paciente=paciente)

    dict_tmp = dict()
    list_tmp = list()

    if len(consulta) > 0:
        for i in consulta:
            dict_tmp["id_pacienteobrasocial"] = i.pk
            dict_tmp["id_obrasocial"] = i.obrasocial.pk
            dict_tmp["descripcion"] = i.obrasocial.descripcion.upper()
            dict_tmp["numeroafiliado"] = i.numeroafiliado
            dict_tmp["observaciones"] = i.observaciones
            list_tmp.append(dict_tmp)
            dict_tmp = dict()

    return JsonResponse(list_tmp, safe=False)


@csrf_exempt
def ajax_editarpacienteobrasocial(request):
    datos = ast.literal_eval(request.POST["datos"])

    paciente_obrasocial = PacienteObraSocial.objects.get(pk=datos["paciente_obrasocial"])
    obraosocial = ObraSocial.objects.get(pk=int(datos["obrasocial"]))
  
    paciente_obrasocial.obrasocial=obraosocial
    paciente_obrasocial.numeroafiliado=datos["numeroafiliado"]
    paciente_obrasocial.observaciones=datos["observaciones"]

    paciente_obrasocial.save()

    paciente = Paciente.objects.get(pk=datos["paciente"])

    paciente_obrasocial = PacienteObraSocial.objects.filter(paciente=paciente)

    dict_tmp = dict()
    list_tmp = list()

    if len(paciente_obrasocial) > 0:
        for i in paciente_obrasocial:
            dict_tmp["id_pacienteobrasocial"] = i.pk
            dict_tmp["id_obrasocial"] = i.obrasocial.pk
            dict_tmp["descripcion"] = i.obrasocial.descripcion.upper()
            dict_tmp["numeroafiliado"] = i.numeroafiliado
            dict_tmp["observaciones"] = i.observaciones
            list_tmp.append(dict_tmp)
            dict_tmp = dict()

    return JsonResponse(list_tmp, safe=False)


def reportelistado(request):
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
            ).order_by('apellido')
        else:
            consulta = Paciente.objects.filter(
                Q(apellido__icontains=parametro) |
                Q(nombre__contains=parametro)
            ).filter(profesional_tratante=usuarioprofesional).order_by('apellido')
            #consulta = consulta.filter(profesional_tratante=usuarioprofesional)            
    else:
        if usuario.is_staff:
            consulta = Paciente.objects.all().order_by('apellido')
        else:
            consulta = Paciente.objects.filter(profesional_tratante=usuarioprofesional).order_by('apellido')

    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'pacientes/reporte_listado.html', {'resultados': resultados})

# Create your views here.
