

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import DatosBancariosForm
from .models import DatosBancarios


@login_required(login_url='/login')
def listadodatosbancarios(request):
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username))
    
    if usuario.is_staff:
        consulta = DatosBancarios.objects.all()
    else:
        consulta = DatosBancarios.objects.filter(usuario=usuario)

    paginador = Paginator(consulta, 20)

    if "page" in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    resultados = paginador.get_page(page)
    return render(
        request,
        'bancos/banco_list.html',
        {
            'resultados': resultados,
            'usuario': usuario
        })


def nuevodatobancario(request):
    """
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username)
    """

    if request.POST:
        form = DatosBancariosForm(request.POST)
        if form.is_valid():
            datobancario = form.save(commit=False)
            datobancario.save()
            messages.success(request, "SE HA GRABADO LOS DATOS BANCARIOS")
            return redirect('/datosbancarioslistado')
    else:
        form = DatosBancariosForm()
        return render(
            request,
            'bancos/banco_edit.html',
            {"form": form}
        )


def editardatobancario(request, pk):
    consulta = DatosBancarios.objects.get(pk=pk)
    if request.user.is_authenticated:
        usuario = User.objects.get(username=str(request.user.username))

    if request.POST:
        form = DatosBancariosForm(request.POST, instance=consulta)
        if form.is_valid():
            datobancario = form.save(commit=False)
            datobancario.usuario = usuario
            datobancario.save()
            messages.success(request, "SE HA GRABADO LOS DATOS BANCARIOS")
            return redirect('/datosbancarioslistado')
    else:
        form = DatosBancariosForm(instance=consulta)
        return render(
            request,
            'bancos/banco_edit.html',
            {"form": form}
        )


# Create your views here.
