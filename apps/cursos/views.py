

from django.contrib import messages
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import CursoForm
from .models import Curso


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


# Create your views here.
