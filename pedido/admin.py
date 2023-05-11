from django.contrib import admin

from pedido.models import Order, Product

# Register your models here.
admin.site.register(Order)
# ! This is not necessary because the product model is already declared in producto\models.py
# admin.site.register(Product)
