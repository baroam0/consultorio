

from .models import Paciente, PacienteObraSocial


def verifica_paciente(numero_documento):
    """Funcion para verificar si existe un paciente con ese dni
    """
    try:
        consulta = Paciente.objects.get(numero_documento=numero_documento)
        existe = True
    except:
        existe = False

    return existe


def verifica_obrasocial(paciente):
    """Funcion para verificar la existencia de una obra social
    """
    consulta = PacienteObraSocial.objects.filter(paciente=paciente)

    if not consulta:
        tiene_obrasocial = False
    else:
        tiene_obrasocial = True
    
    return tiene_obrasocial
    

    """
    my_objects = list(MyModel.objects.filter(published=True))
    if not my_objects:
        raise Http404("No MyModel matches the given query.")
    """

        

    



