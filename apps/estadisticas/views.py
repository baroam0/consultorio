
from django.shortcuts import render

from apps.obrassociales.models import ObraSocial
from apps.profesionales.models import Profesional


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

# Create your views here.
