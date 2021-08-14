
from django import forms

from .models import Curso


class CursoForm(forms.ModelForm):
    descripcion = forms.CharField(label="Descripcion", required=True) 
    duracion = forms.CharField(label="Duracion", required=True)
    valor = forms.CharField(label="Valor", required=True)

    class Meta:
       model = Curso
       fields = ["descripcion", "duracion", "valor", "modalidad"]

    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

