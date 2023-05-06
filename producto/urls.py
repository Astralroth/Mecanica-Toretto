from django.urls import path

from producto.views import ProductFormView 

urlpatterns = [
    path('add', ProductFormView,name='addProduct')
]




