from django import forms

from core.models import Order


class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'name',
            'json',
        )