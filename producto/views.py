import json
from django.shortcuts import render
from producto.models import Product, Provider
from producto.forms import ProductForm
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required

# Create your views here.

def ProductFormView(request):
    data ={
        'form': ProductForm()
    }

    if request.method == "POST":
        formulario = ProductForm(data=request.POST)
        print(request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Producto Registrado"
        else:
            data["form"] = formulario

    return render(request, "producto/registro.html",data)

@method_decorator(
    [csrf_exempt, login_required(redirect_field_name="addOrder", login_url="login")],
    name="dispatch",
)
class ProductListView(TemplateView):
    template_name = "producto/Listado.html"
    
    def post(self, request: HttpRequest):
        action = request.POST["action"]
        if action == "getData":
            productos = Product.objects.all()
            parsed: dict = serialize("json", productos)
            json_v = json.loads(parsed)

            data = []
            for i in range(0, productos.__len__()):
                json_v[i]["fields"]["id"] = json_v[i]["pk"]
                data.append(json_v[i]["fields"])
            
            response = {"data": data}
            return JsonResponse(response, safe=False)
        elif action == "edit":
            data: str = request.POST["data"]
            json_v = json.loads(data)
            
            print(f'JSON: {json_v}')
            id = json_v[0]["value"]
            order = Product(id=id)
            order.nombre = json_v[1]["nombre"]
            order.descripcion = json_v[1]["descripcion"]
            order.provider = Provider.objects.get(id=json_v[1]["provider"])
            order.precio = json_v[1]["precio"]
            order.estado = json_v[1]["estado"]
            order.save()
            # print(f'Order: {order}')
            return JsonResponse({"status": "Redirect", "url": reverse("listProduct")})
        else:
            return JsonResponse({"status":"Error","error": "No se ha encontrado la acción solicitada"})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductForm()
        return context