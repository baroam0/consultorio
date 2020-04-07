from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse

from apps.catalogosenfermedades.models import Catalogo


def ajaxcatalogo(request):
    parametro = request.GET.get('term')

    consulta = Catalogo.objects.filter(
        Q(clave__icontains=parametro) |
        Q(descripcion__icontains=parametro)
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
