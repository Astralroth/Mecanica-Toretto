from django.contrib import admin

from pedido.models import Order, Product

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
