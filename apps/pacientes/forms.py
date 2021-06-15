
from django import forms
from django.contrib.auth.models import User

from .models import TipoDocumento, Paciente
from apps.catalogosenfermedades.models import Catalogo
from apps.obrassociales.models import ObraSocial
from apps.pacientes.models import Paciente, PacienteObraSocial
from apps.profesionales.models import Profesional


class PacienteForm(forms.ModelForm):    

    nombre = forms.CharField(label="Nombre", required=True)
    apellido = forms.CharField(label="Apellido", required=True)
    tipodocumento = forms.ModelChoiceField(
        queryset=TipoDocumento.objects.all(), 
        label="Tipo Documento",
        required=True
    )
    numero_documento = forms.CharField(label="Numero Documento", required=True)
    fecha_nacimiento = forms.DateField(
        label="Fecha Nacimiento", required=False)
    telefono = forms.CharField(label="Telefono", required=False)
    telefono_opcional = forms.CharField(
        label="Telefono Opcional", required=False)
    correo_electronico = forms.EmailField(
        label="Correo Electronico", required=False)
    domicilio = forms.CharField(label="Domicilio", required=False)
    ocupacion = forms.CharField(label="Ocupacion", required=False)
    fecha_admision = forms.DateField(label="Fecha Admision", required=False)
    profesional_tratante = forms.ModelChoiceField(
        queryset=Profesional.objects.all().order_by("usuario__last_name"),
        label = 'Profesional Tratante',
        required=False,
    )
    medicacion = forms.CharField(label="Medicación", required=False)
    fue_al_psicologo = forms.CharField(label="Fue al Psicologo", required=False)
    grupo_familiar = forms.CharField(label="Grupo Familiar", required=False)
    diagnostico =  forms.ModelChoiceField(
        queryset=Catalogo.objects.filter(clave__icontains="F"),
        label = 'Diagnostico',
        required=False,
    )

    observacion = forms.CharField(
        widget=forms.Textarea, label="Observacion", required=False)

    def __init__(self, *args, **kwargs):
        super(PacienteForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'tipodocumento', 'numero_documento',
            'fecha_nacimiento', 'telefono', 'telefono_opcional',
            'correo_electronico', 'domicilio', 'ocupacion', 'fecha_admision',
            'profesional_tratante', 'medicacion', 'fue_al_psicologo',
            'grupo_familiar', 'diagnostico', 'observacion']


class PacienteObraSocialForm(forms.ModelForm):
    """
    paciente = forms.ModelChoiceField(
        queryset=Paciente.objects.all(), 
        label="Paciente",
        required=True
    )
    """
    obrasocial = forms.ModelChoiceField(
        queryset=ObraSocial.objects.all().order_by("descripcion"), 
        label="Obra Social",
        required=True
    )
    numeroafiliado = forms.CharField(
        label="Numero Afiliado", required=False)

    observaciones = forms.CharField(
        widget=forms.Textarea, label="Observaciones", required=False)

    def __init__(self, *args, **kwargs):
        super(PacienteObraSocialForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'style': 'width:100%'
            })

    class Meta:
        model = PacienteObraSocial
        fields = ['obrasocial', 'numeroafiliado', 'observaciones']

