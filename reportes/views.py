from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, JsonResponse
from django.db import models
from core.models import Product


# Create your views here.
class SalesView(TemplateView):
    template_name = 'reportes/ventas.html'
    
    # def get(self, request: HttpRequest):       
    #     products = Product.objects.all().values('nombre', 'cantidad', 'precio')
    #     data = {'data': list(products)}
    #     return JsonResponse(data)