
from django import forms

from .models import Curso, Modulo


class CursoForm(forms.ModelForm):
    descripcion = forms.CharField(label="Descripcion", required=True)
    duracion = forms.CharField(label="Duracion", required=True)
    presencial = forms.BooleanField(label="Presencial")
    virtual = forms.BooleanField(label="Virtual ")

    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field == "descripcion" or field == "duracion":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

    class Meta:
        model = Curso
        fields = ['descripcion', 'duracion', 'presencial', 'virtual']


class ModuloForm(forms.ModelForm):
    descripcion = forms.CharField(label="Descripcion", required=True)
    valor = forms.DecimalField(label="Valor")

    def __init__(self, *args, **kwargs):
        super(ModuloForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field == "descripcion" or field == "duracion":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

    class Meta:
        model = Modulo
        fields = ['descripcion', 'valor']
