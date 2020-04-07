
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import ObraSocialForm, PrestacionForm, NucleadorPrestacionForm
from .models import ObraSocial, Prestacion, NucleadorPrestacion

from django.core.paginator import Paginator
from django.shortcuts import render


def obrasociallistado(request):
    if 'txtBuscar' in request.GET:
        parametro = request.GET.get('txtBuscar')
        consulta = ObraSocial.objects.filter(
            Q(descripcion__icontains=parametro) |
            Q(abreviatura__icontains=parametro)
        ).order_by('descripcion')
    else:
        consulta = ObraSocial.objects.all().order_by('descripcion')
    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'obrassociales/obrasocial_list.html', {'resultados': resultados})


def nuevaobrasocial(request):
    if request.POST:
        form = ObraSocialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO LA OBRA SOCIAL")
            return redirect('/obrasociallistado')
        else:
            return render(request, 'obrassociales/obrasocial_edit.html', {"form": form})
    else:
        form = ObraSocialForm()
        return render(request, 'obrassociales/obrasocial_edit.html', {"form": form})


def editarobrasocial(request, pk):
    consulta = ObraSocial.objects.get(pk=pk)
    if request.POST:
        form = ObraSocialForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO LA OBRA SOCIAL")
            return redirect('/obrasociallistado')
        else:
            return render(request, 'obrassociales/obrasocial_edit.html', {"form": form})
    else:
        form = ObraSocialForm(instance=consulta)
        return render(request, 'obrassociales/obrasocial_edit.html', {"form": form})


def prestacionlistado(request):
    if 'txtBuscar' in request.GET:
        parametro = request.GET.get('txtBuscar')
        consulta = Prestacion.objects.filter(
            Q(descripcion__icontains=parametro) |
            Q(codigo__icontains=parametro)
        ).order_by('descripcion')
    else:
        consulta = Prestacion.objects.all().order_by('descripcion')
    paginador = Paginator(consulta, 5)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'obrassociales/prestacion_list.html', {'resultados': resultados})


def nuevaprestacion(request):
    if request.POST:
        form = PrestacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO LA PRESTACION")
            return redirect('/prestacionlistado')
        else:
            return render(request, 'obrassociales/prestacion_edit.html', {"form": form})
    else:
        form = PrestacionForm()
        return render(request, 'obrassociales/prestacion_edit.html', {"form": form})


def editarprestacion(request, pk):
    consulta = Prestacion.objects.get(pk=pk)
    if request.POST:
        form = PrestacionForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO LA PRESTACION")
            return redirect('/prestacionlistado')
        else:
            return render(request, 'obrassociales/prestacion_edit.html', {"form": form})
    else:
        form = PrestacionForm(instance=consulta)
        return render(request, 'obrassociales/prestacion_edit.html', {"form": form})


def nucleadorprestacionlistado(request):
    if 'txtBuscar' in request.GET:
        parametro = request.GET.get('txtBuscar')
        consulta = NucleadorPrestacion.objects.filter(
            Q(nucleador__descripcion__contains=parametro) |
            Q(obrasocial__descripcion__contains=parametro) |
            Q(obrasocial__abreviatura__contains=parametro) |
            Q(prestacion__descripcion__contains=parametro) |
            Q(prestacion__codigo__contains=parametro)
        )
    else:
        consulta = NucleadorPrestacion.objects.all()
    paginador = Paginator(consulta, 20)
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(request, 'obrassociales/nucleadorprestacion_list.html', {'resultados': resultados})


def nuevonucleadorprestacion(request):
    if request.POST:
        form = NucleadorPrestacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO LA PRESTACION")
            return redirect('/nucleadorprestacionlistado')
        else:
            return render(request, 'obrassociales/nucleadorprestacion_edit.html', {"form": form})
    else:
        form = NucleadorPrestacionForm()
        return render(request, 'obrassociales/nucleadorprestacion_edit.html', {"form": form})


def editarnucleadorprestacion(request, pk):
    consulta = NucleadorPrestacion.objects.get(pk=pk)
    if request.POST:
        form = NucleadorPrestacionForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO LA PRESTACION")
            return redirect('/nucleadorprestacionlistado')
        else:
            return render(request, 'obrassociales/nucleadorprestacion_edit.html', {"form": form})
    else:
        form = NucleadorPrestacionForm(instance=consulta)
        return render(request, 'obrassociales/nucleadorprestacion_edit.html', {"form": form})


def ajaxobrasocial(request):
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


# Create your views here.
