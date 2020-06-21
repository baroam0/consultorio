
from datetime import datetime
from apps.pacientes.models import Paciente


def cumple_paciente(request):

    try:
        mes = datetime.today().month
        dia = datetime.today().day
        cumplepaciente = Paciente.objects.filter(
            fecha_nacimiento__month=mes,
            fecha_nacimiento__day=dia
        )

        return {
            "cumplepaciente": cumplepaciente
        }
    except:
        return {
            "cumplepaciente": ""
        }
