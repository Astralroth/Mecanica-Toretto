from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .forms import CreationTicketForm
from core.models import Servicio


class ServicioListView(ListView):
    model = Servicio
    template_name = 'servicio_list.html'

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
    

class ServicePaymentView(TemplateView):
    template_name = 'Boleta/addTicket.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreationTicketForm()
        return context
    
