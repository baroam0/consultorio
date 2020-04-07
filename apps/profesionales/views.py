
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import Profesional
from .forms import ProfesionalForm, UsuarioForm


def listadoprofesional(request):
    if "txtBuscar" in request.GET:
        parametro = request.GET.get('txtBuscar')
        consulta = Profesional.objects.filter(
            Q(usuario__last_name__contains=parametro) | 
            Q(usuario__first_name__contains=parametro)
        )
    else:
        consulta = Profesional.objects.all()
    paginador = Paginator(consulta, 20)
    
    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)

    return render(request, 'profesionales/profesional_list.html', {'resultados': resultados})


def perfil(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username))
    try:
        profesional = Profesional.objects.get(usuario=usuario)
    except Profesional.DoesNotExist:
        profesional = None

    if request.POST:
        if profesional:
            profesional = Profesional.objects.get(
                usuario=usuario.profesional.pk
            )
            form_user = UsuarioForm(request.POST, instance=usuario)
            form = ProfesionalForm(request.POST, instance=profesional)
            if form_user.is_valid:
                if form.is_valid():
                    form_user.save()
                    form.save()
                    messages.success(request,"SE HAN GUARDADO EL PROFESIONAL")
                    return redirect('/')
        else:
            form_user = UsuarioForm(
                request.POST, instance=usuario)
            form = ProfesionalForm(request.POST)
            if form_user.is_valid():
                form_user.save()
                if form.is_valid:
                    form.save()                    
                    messages.success(request,"SE HAN GUARDADO EL PROFESIONAL")
                    return redirect('/')
    else:
        form_user = UsuarioForm(instance=usuario)
        try:
            profesional = Profesional.objects.get(usuario=usuario)
        except Profesional.DoesNotExist:
            profesional = None

        if profesional is not None:
            profesional = Profesional.objects.get(usuario=usuario)
            form = ProfesionalForm(instance=profesional)
        else:
            form = ProfesionalForm()

        return render(
            request,
            'profesionales/profesional_edit.html',
            {
                "form": form,
                "form_user": form_user,
            }
        )


def editarprofesional(request, pk):
    consulta = Profesional.objects.get(pk=pk)
    if request.POST:
        form = ProfesionalForm(request.POST, instance=consulta)
        if form.is_valid:
            profesional = form.save()
            messages.success(request, "SE HAN ACTUALIZADO EL PROFESIONAL")
            return redirect('/profesionallistado')
    else:
        form = ProfesionalForm(instance=consulta)
        return render(
            request,
            'profesionales/profesional_edit.html',
            {"form": form}
        )


# Create your views here.
