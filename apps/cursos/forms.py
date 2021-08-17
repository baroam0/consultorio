
from django import forms

from .models import Curso


class CursoForm(forms.ModelForm):
   descripcion = forms.CharField(label="Descripcion", required=True) 
   duracion = forms.CharField(label="Duracion", required=True)
   presencial = forms.BooleanField(required=False)
   virtual = forms.BooleanField(required=False)

   
   def __init__(self, *args, **kwargs):
       super(CursoForm,self).__init__(*args, **kwargs)
     
       for field in iter(self.fields):
           if self.fields[field].widget.input_type != "checkbox":
               self.fields[field].widget.attrs.update({
                   'class' : 'form-control'
                })
    

   class Meta:
       model = Curso
       fields = ["descripcion", "duracion", "presencial", "virtual"]
