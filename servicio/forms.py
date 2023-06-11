from django import forms
from core.models import Boleta, Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'tiempo_estimado', 'productos_asociados']

class CreationTicketForm(forms.ModelForm):
    
    # Desactiva subtotal, impuesto y total
    subtotal = forms.DecimalField(disabled=True)
    impuesto = forms.DecimalField(disabled=True)
    total = forms.DecimalField(disabled=True)
    
    
    class Meta:
        model = Boleta
        fields = ['service', 'order','firstname','lastname','run','subtotal','impuesto','total']