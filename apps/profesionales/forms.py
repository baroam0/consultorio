
from django import forms
from django.contrib.auth.models import User


from .models import Especialidad, Profesional


class UsuarioNombreApellido(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", required=True)
    last_name = forms.CharField(label="Apellido", required=True)

    def __init__(self, *args, **kwargs):
        super(UsuarioNombreApellido, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Profesional
        fields = ['first_name', 'last_name']

    
class ProfesionalForm(forms.ModelForm):
    

    """
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label = 'Usuario',
    )
    """
    
    especialidad = forms.ModelMultipleChoiceField(
        queryset=Especialidad.objects.all(),
        required=False,
        label = 'Especialidad',
    )
    numero_prestador = forms.IntegerField(label="Numero Prestador", required=False)
    numero_prestador_vencimiento = forms.DateField(label="Vecimiento", required=False)
    telefono = forms.CharField(label="Telefono", required=True)
    telefono_opcional = forms.CharField(label="Telefono Opcional", required=False)
    observacion = forms.CharField(widget=forms.Textarea, label="Observacion", required=False)

    def __init__(self, *args, **kwargs):
        super(ProfesionalForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Profesional
        fields = ['especialidad', 'numero_prestador',
            'numero_prestador_vencimiento', 'telefono',
            'telefono_opcional', 'observacion']
