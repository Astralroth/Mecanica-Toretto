from django.shortcuts import render
from producto.models import Product
from producto.forms import ProductForm

# Create your views here.

def ProductFormView(request):
    data ={
        'form': ProductForm()
    }

    if request.method == "POST":
        formulario = ProductForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Producto Registrado"
        else:
            data["form"] = formulario

    return render(request, "producto/registro.html",data)

