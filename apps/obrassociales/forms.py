
from django import forms

from .models import Nucleador, NucleadorPrestacion, ObraSocial, Prestacion


class ObraSocialForm(forms.ModelForm):
    descripcion = forms.CharField(label="Descripcion", required=True)
    abreviatura = forms.CharField(label="Abreviatura", required=False)
    telefono = forms.CharField(label="Telefono", required=True)
    telefono_opcional = forms.CharField(label="Telefono Opcional", required=False)
    correo_electronico = forms.EmailField(label="Correo Electronico", required=False)
    observacion = forms.CharField(widget=forms.Textarea, label="Observacion", required=False)

    def __init__(self, *args, **kwargs):
        super(ObraSocialForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = ObraSocial
        fields = ['descripcion', 'abreviatura', 'telefono', 'telefono_opcional', 'correo_electronico', 'observacion']


class PrestacionForm(forms.ModelForm):
    codigo = forms.CharField(label="Codigo", required=True)
    descripcion = forms.CharField(label="Descripcion", required=True)

    def __init__(self, *args, **kwargs):
        super(PrestacionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Prestacion
        fields = ['codigo', 'descripcion']


class NucleadorPrestacionForm(forms.ModelForm):
    nucleador = forms.ModelChoiceField(
        queryset=Nucleador.objects.all(),
        label="Nucleador"
    )
    obrasocial = forms.ModelChoiceField(
        queryset=ObraSocial.objects.all(),
        label="Obra Social" 
    )
    prestacion = forms.ModelChoiceField(
        queryset=Prestacion.objects.all()
    )
    importe = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        super(NucleadorPrestacionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = NucleadorPrestacion
        fields = ['nucleador', 'obrasocial', 'prestacion', 'importe']

