from django import forms

from producto.models import Product


class ProductForm(forms.ModelForm):
    provedor = forms.CharField(widget=forms.HiddenInput, max_length=50, required=False, label='')
    class Meta:
        model = Product
        fields = ('nombre',
                  'descripcion',
                  'provider',
                  'precio',
                  'estado'
                  )
        