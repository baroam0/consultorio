

from django.core.paginator import Paginator
from django.shortcuts import render

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
    if resquest.POST:

        




# Create your views here.
