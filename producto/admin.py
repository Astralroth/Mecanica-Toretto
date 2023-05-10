from django.contrib import admin

from .models import Product, Provider, producto_boleta

# Register your models here.

admin.site.register(Product)
admin.site.register(Provider)
admin.site.register(producto_boleta)