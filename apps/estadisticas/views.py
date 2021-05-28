

from django.http import JsonResponse
from django.shortcuts import render

from apps.obrassociales.models import ObraSocial
from apps.profesionales.models import Profesional
from apps.turnos.models import Turno


def estadisticaasistencial(request):
    return render(request, 'estadisticas/estadistica_obrasocial.html')


def estadisticaobrasocialmes(request):
    obrassociales = ObraSocial.objects.all().order_by("abreviatura")
    profesionales = Profesional.objects.all()

    return render(
        request,
        'estadisticas/reporteobrasocialmes.html',
        {
            'obrassociales': obrassociales,
            'profesionales': profesionales
        })


def estadisticaconsultatotalturnos(request):

    if request.method=="GET":
        obrasocial = ObraSocial.objects.get(pk=request.GET.get("obrasocial"))
        profesional = Profesional.objects.get(pk=request.GET.get("profesional"))
        mes = request.GET.get("mes")
        anio = request.GET.get("anio")

        consulta = Turno.objects.filter(
            fechahora__month=mes,
            fechahora__year=anio,
            obrasocial = obrasocial,
            profesional = profesional,
        ).count()

        return JsonResponse(consulta, safe=False)    
    

# Create your views here.
