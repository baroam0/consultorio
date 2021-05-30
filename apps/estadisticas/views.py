

from django.db.models import Count
from django.core import serializers
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

        turnosotorgados = Turno.objects.filter(
            fechahora__month=mes,
            fechahora__year=anio,
            obrasocial = obrasocial,
            profesional = profesional,
        ).count()

        turnosasistidos = Turno.objects.filter(
            fechahora__month=mes,
            fechahora__year=anio,
            obrasocial = obrasocial,
            profesional = profesional,
            asistio = True
        ).count()

        turnosentregas = Turno.objects.filter(
            fechahora__month=mes,
            fechahora__year=anio,
            obrasocial = obrasocial,
            profesional = profesional,
            asistio = True,
            entrega = True
        ).count()

        turnosentregaparcial = Turno.objects.filter(
            fechahora__month=mes,
            fechahora__year=anio,
            obrasocial = obrasocial,
            profesional = profesional,
            asistio = True,
            entrega = False,
            entrega_parcial = True
        ).count()

        turnossinorden = Turno.objects.filter(
            fechahora__month=mes,
            fechahora__year=anio,
            obrasocial = obrasocial,
            profesional = profesional,
            entrega = False,
            entrega_parcial = False
        ).count()

        turnosinasistidos = Turno.objects.filter(
            fechahora__month=mes,
            fechahora__year=anio,
            obrasocial = obrasocial,
            profesional = profesional,
            asistio = False,
        ).count()

        data = {
            "turnosotorgados": turnosotorgados,
            "turnosasistidos": turnosasistidos,
            "turnosentregas": turnosentregas,
            "turnosentregaparcial":turnosentregaparcial,
            "turnossinorden": turnossinorden,
            "turnosinasistidos": turnosinasistidos
        }        

        return JsonResponse(data, safe=False)


# Create your views here.
