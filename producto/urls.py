from django.urls import path

from producto.views import ProductFormView, ProductListView

from . import views

urlpatterns = [
    path('add', ProductFormView, name='addProduct'),
    path('list', ProductListView.as_view(), name='listProduct'),
    
]




