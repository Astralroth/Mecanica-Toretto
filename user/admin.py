from django.contrib import admin
from .models import User, products, observaciones
from django.contrib.auth.admin import UserAdmin

admin.site.register(User)
admin.site.register(observaciones)
admin.site.register(products)