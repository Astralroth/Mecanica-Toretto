import json
from django.http import HttpRequest, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse, reverse_lazy
from .forms import CreationTicketForm
from core.models import Boleta, Servicio
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class ServicioListView(ListView):
    model = Servicio
    template_name = 'servicio/servicio_list.html'

class ServicioCreateView(CreateView):
    model = Servicio
    template_name = 'servicio/registrar_servicio.html' 
    fields = ['nombre', 'descripcion', 'precio', 'tiempo_estimado', 'productos_asociados']
    success_url = reverse_lazy('listar_servicios')


class ServicioUpdateView(UpdateView):
    model = Servicio
    template_name = 'servicio/modificar_servicio.html' 
    fields = ['nombre', 'descripcion', 'precio', 'tiempo_estimado', 'productos_asociados']
    success_url = reverse_lazy('listar_servicios')

class ServicioDeleteView(DeleteView):
    model = Servicio
    template_name = 'servicio/eliminar_servicio.html'  
    success_url = reverse_lazy('listar_servicios')
    

@method_decorator(
    [csrf_exempt, login_required(redirect_field_name="pago_servicio", login_url="login")],
    name="dispatch",
)
class ServicePaymentView(TemplateView):
    template_name = 'Boleta/addTicket.html'
    
    def post(self, request: HttpRequest):
        action = request.POST["action"]
        if action == "getData":
            response = {}
            
            allServ = Servicio.objects.all()
            parsedProds: dict = serialize("json", allServ)
            json_v = json.loads(parsedProds)
            
            dataProd = []
            for i in range(0, allServ.__len__()):
                json_v[i]["fields"]["id"] = json_v[i]["pk"]
                dataProd.append(json_v[i]["fields"])
            
            response['services']=dataProd
            return JsonResponse(response, safe=False)
        elif action == "addTicket":
            data: str = request.POST["data"]
            json_v = json.loads(data)
            
            print(f'JSON: {json_v}')
            order = Boleta.objects.create(
                firstname = json_v[0]["firstname"],
                lastname = json_v[0]["lastname"],
                run = json_v[0]["run"],
                subtotal = json_v[0]["subtotal"],
                impuesto = json_v[0]["tax"],
                total = json_v[0]["total"],
            )
            
            print(json_v[0]["service"])
            
            for i in json_v[0]["service"]:
                order.service.add(Servicio.objects.get(pk=i))
        
            order.save()
            # print(f'Order: {order}')
            
            # TODO: Cambiar la redireccion con la lista de pago de servicios u similar
            return JsonResponse({"status": "Redirect", "url": reverse("listOrder")})
        else:
            return JsonResponse({"status":"Error","error": "No se ha encontrado la acción solicitada"})
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreationTicketForm()
        return context
    
