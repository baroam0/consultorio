
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Especialidad, Profesional


class UsuarioForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre",  max_length=30)
    last_name = forms.CharField(label="Apellido", max_length=30)

    class Meta:
        model = User
        #fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ProfesionalForm(forms.ModelForm):    
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


