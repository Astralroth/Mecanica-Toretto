from django.contrib import admin

from .models import Product, Provider

# Register your models here.

admin.site.register(Product)
admin.site.register(Provider)
