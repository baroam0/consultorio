
from django import forms


from apps.obrassociales.models import ObraSocial
from apps.pacientes.models import Paciente
from apps.profesionales.models import Profesional
from apps.turnos.models import Turno


class TurnoForm(forms.ModelForm):
    
    fechahora = forms.DateTimeField(
        label="Fecha / Hora(*)",
        required=True,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'dd/mm/aa hh:mm'
        })
    )

    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(), 
        label="Paciente",
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    obrasocial = forms.ModelChoiceField(
        queryset=ObraSocial.objects.all(), 
        label="Obra Social",
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    profesional = forms.ModelChoiceField(
        queryset=Profesional.objects.all(), 
        label="Profesional",
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    asistio = forms.BooleanField(
        required=False
    )

    entrega = forms.BooleanField(
        required=False
    )

    entrega_parcial = forms.BooleanField(
        required=False
    )

    observacion = forms.CharField(
        label="Observacion",
        required=False,
        widget=forms.Textarea(
            attrs={'class': 'form-control'}
        ))

    class Meta:
        model = Turno
        fields = ['fechahora', 'paciente', 'obrasocial', 'profesional',
            'asistio', 'entrega', 'entrega_parcial', 'observacion']
