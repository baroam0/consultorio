from django.shortcuts import render


def listadoturno(request):
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



# Create your views here.
