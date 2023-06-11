from django import forms
from core.models import Boleta, Servicio


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
    service = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=Servicio.objects.all().values_list("id", "nombre"),
        required=True,
    )

    firstname = forms.CharField(max_length=50, required=False)
    lastname = forms.CharField(max_length=50, required=False)
    run = forms.CharField(max_length=8, required=False)

    tipo = forms.ChoiceField(
        choices=[("boleta", "Boleta"), ("factura", "Factura")], required=True
    )

    # Desactiva subtotal, impuesto y total
    subtotal = forms.DecimalField(disabled=True)
    impuesto = forms.DecimalField(disabled=True)
    total = forms.DecimalField(disabled=True)
