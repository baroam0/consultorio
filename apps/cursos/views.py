

from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import AlumnoForm, CursoForm, ModuloForm, InscripcionForm
from .models import Alumno, Curso, Modulo, Inscripcion


def listadocurso(request):
    if 'txtBuscar' in request.GET:
        parametro = request.GET.get('txtBuscar')
        consulta = Curso.objects.filter(descripcion__icontains=parametro).order_by('descripcion')
    else:
        consulta = Curso.objects.all().order_by('descripcion')
    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'cursos/curso_list.html', {'resultados': resultados})


def nuevocurso(request):
    if request.POST:
        form = CursoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "SE HA GRABADO EL CURSO")
                return redirect('/listadocurso')
            except IntegrityError as e:
                messages.success(request, "YA EXISTE UN CURSO CON ESE NOMBRE.")
                return render(request, 'cursos/curso_nuevo.html', {"form": form})    
        else:
            return render(request, 'cursos/curso_nuevo.html', {"form": form})
    else:
        form = CursoForm()
        return render(request, 'cursos/curso_nuevo.html', {"form": form})


def editarcurso(request, pk):
    consulta = Curso.objects.get(pk=pk)
    if request.POST:
        form = CursoForm(request.POST, instance=consulta)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "SE HA ACTUALIZADO LOS DATOS DEL CURSO")
                return redirect('/listadocurso')
            except IntegrityError as e:
                messages.success(request, "YA EXISTE UN CURSO CON ESE NOMBRE.")
                return render(request, 'cursos/curso_nuevo.html', {"form": form})
        else:
            return render(request, 'cursos/curso_edit.html', {"form": form})
    else:
        form = CursoForm(instance=consulta)
        return render(request, 'cursos/curso_edit.html', {"form": form})


def listadomodulo(request, pk):
    curso = Curso.objects.get(pk=pk)
    modulos = Modulo.objects.filter(curso=pk)
    return render(request, 'cursos/modulo_list.html',
        {
            'curso': curso,
            'modulos': modulos
        }
    )


def nuevomodulo(request, pk):
    curso = Curso.objects.get(pk=pk)
    if request.POST:
        form = ModuloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO EL MODULO")
            return redirect('/listadocurso')
        else:
            return render(request, 'cursos/modulo_edit.html', {"form": form})
    else:
        form = ModuloForm()
        return render(request, 'cursos/modulo_edit.html', {"form": form, "curso":curso})


def editarmodulo(request, pk):
    consulta = Modulo.objects.get(pk=pk)
    if request.POST:
        form = ModuloForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO LOS DATOS DEL MODULO")
            return redirect('/listadocurso')
        else:
            return render(request, 'cursos/modulo_edit.html', {"form": form})
    else:
        form = ModuloForm(instance=consulta)
        return render(request, 'cursos/modulo_edit.html', {"form": form})


def listadoalumno(request):
    if 'txtBuscar' in request.GET:
        parametro = request.GET.get('txtBuscar')
        consulta = Alumno.objects.filter(
            Q(apellido__icontains=parametro) |
            Q(nombre__contains=parametro) |
            Q(numerodocumento__contains=parametro)
        ).order_by('apellido')
    else:
        consulta = Alumno.objects.all().order_by('apellido')
    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'cursos/alumno_list.html', {'resultados': resultados})


def nuevoalumno(request):
    if request.POST:
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO EL ALUMNO")
            return redirect('/listadoalumno')
        else:
            return render(request, 'cursos/alumno_edit.html', {"form": form})
    else:
        form = AlumnoForm()
        return render(request, 'cursos/alumno_edit.html', {"form": form})


def editaralumno(request, pk):
    consulta = Alumno.objects.get(pk=pk)
    if request.POST:
        form = AlumnoForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO LOS DATOS DEL CURSO")
            return redirect('/listadocurso')
        else:
            return render(request, 'cursos/alumno_edit.html', {"form": form})
    else:
        form = AlumnoForm(instance=consulta)
        return render(request, 'cursos/alumno_edit.html', {"form": form})


def listadoinscripcion(request):
    if 'txtBuscar' in request.GET:
        parametro = request.GET.get('txtBuscar')
        consulta = Inscripcion.objects.select_related('alumno').filter(
            Q(apellido__icontains=parametro) |
            Q(nombre__contains=parametro)
        ).order_by('fecha')
    else:
        consulta = Inscripcion.objects.all().order_by('fecha')
    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'cursos/inscripcion_list.html', {'resultados': resultados})


def nuevainscripcion(request):
    if request.POST:
        form = InscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO LA INSCRIPCION")
            return redirect('/listadoinscripcion')
        else:
            return render(request, 'cursos/inscripcion_edit.html', {"form": form})
    else:
        form = InscripcionForm()
        return render(request, 'cursos/inscripcion_edit.html', {"form": form})


def editarinscripcion(request, pk):
    consulta = Inscripcion.objects.get(pk=pk)
    if request.POST:
        form = InscripcionForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO LOS DATOS DE LA INSCRIPCION")
            return redirect('/listadoinscripcion')
        else:
            return render(request, 'cursos/inscripcion_edit.html', {"form": form})
    else:
        form = InscripcionForm(instance=consulta)
        return render(request, 'cursos/inscripcion_edit.html', {"form": form})
# Create your views here.
