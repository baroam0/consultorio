
from django import forms

from apps.pacientes.models import TipoDocumento

from .models import Alumno, Curso, Modulo, Profesion, Inscripcion


class CursoForm(forms.ModelForm):
    descripcion = forms.CharField(label="Descripcion", required=True)
    duracion = forms.CharField(label="Duracion", required=True)
    presencial = forms.BooleanField(label="Presencial", required=False)
    virtual = forms.BooleanField(label="Virtual", required=False)

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

    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(), 
        label="Curso",
        required=True
    )
    valor = forms.DecimalField(label="Valor")
    finalizado = forms.BooleanField(
        label="Finalizado", required=False
    )

    def __init__(self, *args, **kwargs):
        super(ModuloForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != "finalizado":
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

    class Meta:
        model = Modulo
        fields = ['descripcion', 'curso', 'valor', 'finalizado']


class AlumnoForm(forms.ModelForm):
    nombre = forms.CharField(label="Nombre", required=True)
    apellido = forms.CharField(label="Apellido", required=True)
    tipodocumento = forms.ModelChoiceField(
        label="Tipo Documento", queryset=TipoDocumento.objects.all()
    )
    numerodocumento = forms.IntegerField(label="Numero de Documento")
    profesion = forms.ModelChoiceField(
        label="Profesion", queryset=Profesion.objects.all()
    )
    matricula = forms.IntegerField(label="Matricula")
    telefono = forms.CharField(label="Telefono", required=True)
    email = forms.EmailField(label="Correo Electronico", required=False)

    def __init__(self, *args, **kwargs):
        super(AlumnoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Alumno
        fields = ['apellido', 'nombre', 'tipodocumento', 'numerodocumento',
            'profesion', 'matricula', 'telefono', 'email']


class InscripcionForm(forms.ModelForm):
    alumno = forms.ModelChoiceField(
        label="Alumno", queryset=Alumno.objects.all().order_by('apellido'))
    modulo = forms.ModelChoiceField(
        label="Modulo", queryset=Modulo.objects.filter(finalizado=False)
    )
    pagado = forms.BooleanField(label="Pagado", required=False)

    def __init__(self, *args, **kwargs):
        super(InscripcionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if field != "pagado" :
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

    class Meta:
        model = Inscripcion
        fields = ['alumno', 'modulo', 'pagado']
