
from django.shortcuts import render


def estadisticaasistencial(request):
    return render(request, 'estadisticas/estadistica_obrasocial.html')


def estadisticaobrasocialmes(request):
    return render(request, 'estadisticas/reporteobrasocialmes.html')

# Create your views here.
