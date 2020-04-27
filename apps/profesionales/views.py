
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as UsuarioForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from .models import Profesional
from .forms import ProfesionalForm


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
        
        form_user = UsuarioForm(request.POST)
        form = ProfesionalForm(request.POST)
        return render(
            request,
            'profesionales/profesional_edit.html',
            {
                "form": form,
                "form_user": form_user,
            }
        )
    else:
        form_user = UsuarioForm(instance=usuario)
        form = ProfesionalForm()
        return render(
            request,
            'profesionales/profesional_edit.html',
            {
                "form": form,
                "form_user": form_user,
            }
        )


def crearprofesional(request):
    if request.POST:
        form_usuario = UsuarioForm(request.POST)
        form = ProfesionalForm(request.POST)
        if form_usuario.is_valid and form.is_valid:
            nombre = request.POST.get('first_name')
            apellido = request.POST.get('last_name')
            usuario = form_usuario.save()
            usuario = User.objects.latest('pk')
            usuario.last_name = apellido
            usuario.first_name = nombre
            usuario.save()

            profesional = form.save(commit=False)
            profesional.usuario = usuario
            profesional.save()

            messages.success(request, "SE HAN ACTUALIZADO EL PROFESIONAL")
            return redirect('/profesionallistado')
        else:
            return render(
                request,
                'profesionales/profesional_edit.html',
                {"form": form}
            )
    else:
        form_usuario = UsuarioForm()
        form = ProfesionalForm()
        return render(
            request,
            'profesionales/profesional_edit.html',
            {
                "form_usuario": form_usuario,
                "form": form
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
