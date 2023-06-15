from django import forms
from core.models import Servicio
from django.shortcuts import get_object_or_404


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "nombre",
            "descripcion",
            "precio",
            "tiempo_estimado",
            "productos_asociados",
        ]


class CreationTicketForm(forms.Form):
    
    service = forms.ChoiceField(required=True, label="Servicio")
    firstname = forms.CharField(max_length=50, required=False, label="Nombre o Razón Social")
    lastname = forms.CharField(max_length=50, required=False, label="Apellido")
    
    run = forms.CharField(max_length=10, min_length=10, required=True, label="Run / Rut")

    # Desactiva subtotal, impuesto y total
    subtotal = forms.DecimalField(disabled=True)
    impuesto = forms.DecimalField(disabled=True)
    total = forms.DecimalField(disabled=True)
