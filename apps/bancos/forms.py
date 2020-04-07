
from django import forms
from django.contrib.auth.models import User
from .models import DatosBancarios, Banco, TipoCuenta, Titular


class DatosBancariosForm(forms.ModelForm):
   
    """
    banco = forms.ModelChoiceField(
        queryset=Banco.objects.all(),
        label="Banco"
    )
    tipocuenta = forms.ModelChoiceField(
        queryset=TipoCuenta.objects.all(),
        label="Tipos de Cuenta"
    )
    cbu = forms.CharField(
        label="CBU", 
        required=True
    )
    """

    titular = forms.ModelChoiceField(
        queryset=Titular.objects.all().exclude(username="admin"),
        required=True)

    def __init__(self, *args, **kwargs):
        super(DatosBancariosForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = DatosBancarios
        fields = ["titular", "banco", "tipocuenta", "cbu"]


