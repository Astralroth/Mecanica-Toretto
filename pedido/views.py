import json

from django.shortcuts import redirect

from pedido.forms import OrderCreationForm

from .models import Order, Product

from django.core.serializers import serialize
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


# Create your views here.
# @method_decorator(
#     [csrf_exempt, login_required(login_url="login", redirect_field_name="next")],
#     name="dispatch",
# )
@method_decorator(
    csrf_exempt,
    name="dispatch",
)
class OrderListView(TemplateView):
    template_name = "pedido/list_order.html"

    def post(self, request: HttpRequest):
        action = request.POST["action"]
        if action == "getData":
            productos = Order.objects.filter(user=request.user)
            parsed: dict = serialize("json", productos)
            json_v = json.loads(parsed)

            data = []
            for i in range(0, productos.__len__()):
                json_v[i]["fields"]["id"] = json_v[i]["pk"]
                data.append(json_v[i]["fields"])
            
            response = {"data": data}
            
            allProds = Product.objects.all()
            parsedProds: dict = serialize("json", allProds)
            prods_v = json.loads(parsedProds)
            
            dataProd = []
            for i in range(0, allProds.__len__()):
                dataProd.append(prods_v[i]["fields"]['name'])
            
            print(dataProd)
            response['products']=dataProd
            return JsonResponse(response, safe=False)
        elif action == "edit":
            print("Editing row")
            data: str = request.POST["data"]
            json_v = json.loads(data)
            id = json_v[0]["value"]
            producto = Order.objects.get(id=id)
            producto.json = json_v[1]

            producto.save()
            return JsonResponse({"status": "Correct"})
        else:
            return JsonResponse({"error": "No se ha encontrado la acción solicitada"})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = OrderCreationForm()
        return context


@method_decorator(
    csrf_exempt,
    name="dispatch",
)
class OrderCreateView(TemplateView):
    template_name = "pedido/reg_order.html"
    
    def post(self, request: HttpRequest):
        action = request.POST["action"]
        if action == "getData":
            response = {}
            
            allProds = Product.objects.all()
            parsedProds: dict = serialize("json", allProds)
            prods_v = json.loads(parsedProds)
            
            dataProd = []
            for i in range(0, allProds.__len__()):
                dataProd.append(prods_v[i]["fields"]['name'])
            
            response['products']=dataProd
            return JsonResponse(response, safe=False)
        elif action == "addOrder":
            # JS3-ASD
            # [{'name': 'JS3-ASD'}, [{'product': 'Aceite para Motor', 'quantity': 1}]]
            data: str = request.POST["data"]
            json_v = json.loads(data)
            print(f'JSON: {json_v}')
            order = Order()
            order.user = request.user
            order.name = json_v[0]["name"]
            order.json = json_v[1]
            order.save()
            print(f'Order: {order}')
            return redirect('listOrder')
        else:
            return JsonResponse({"error": "No se ha encontrado la acción solicitada"})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = OrderCreationForm()
        return context
