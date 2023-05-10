import json
from .models import producto_boleta
from reportlab.pdfgen import canvas
from django.shortcuts import render
from producto.models import Product, Provider
from producto.forms import ProductForm
from django.http import HttpRequest, JsonResponse, HttpResponse
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

#Boleta 
    def post(self, request: HttpRequest):
        action = request.POST["action"]
        if action == "getData":
            productos = Product.objects.all()
            parsed: dict = serialize("json", productos)
            json_v = json.loads(parsed)
            
            # print(f'JSON: {json_v}')
            
            data = []
            for i in range(0, productos.__len__()):
                json_v[i]["fields"]["id"] = json_v[i]["pk"]
                data.append(json_v[i]["fields"])

            # print(f'Data: {data}')
            
            provider = Provider.objects.all()
            prov_parsed: dict = serialize("json", provider)
            json_p = json.loads(prov_parsed)
            
            # print(f'JSON: {json_p}')
            
            data_provider = []
            for i in range(0, provider.__len__()):
                data_provider.append({"user": json_p[i]["pk"], "nombre": json_p[i]["fields"]["nombre"]})
            
            # print(f'Data: {data_provider}')
            
            response = {"data": data, "provider": data_provider}

            return JsonResponse(response, safe=False)
        elif action == "edit":
            data: str = request.POST["data"]
            json_v = json.loads(data)
            
            # print(f'JSON: {json_v}')
            id = json_v[0]["value"]
            prod = Product.objects.get(id=id)
            prod.nombre = json_v[1]["nombre"]
            prod.descripcion = json_v[1]["descripcion"]
            prod.provider = Provider.objects.get(id=json_v[1]["provider"])
            prod.precio = json_v[1]["precio"]
            prod.estado = json_v[1]["estado"]
            prod.save()
            print(f'Prod: {prod}')
            return JsonResponse({"status": "Correcto", "message": "Se ha editado el pedido correctamente"})
        else:
            return JsonResponse({"status":"Error","error": "No se ha encontrado la acción solicitada"})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ProductForm()
        return context

def generar_factura(request, producto_id):
    # Obtenemos la información del producto a través de su ID
    producto = producto_boleta.objects.get(id=producto_id)

    # Creamos un objeto HttpResponse con el tipo de contenido correcto
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="factura{}.pdf"'.format(producto.id)

    # Creamos el objeto PDF, usando el objeto HttpResponse como su "archivo".
    p = canvas.Canvas(response)

    # Agregamos el encabezado de la factura
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(300, 700, "Factura")

    # Agregamos la información del producto
    p.setFont("Helvetica", 12)
    p.drawString(50, 650, "Nombre del producto: {}".format(producto.nombre))
    p.drawString(50, 625, "Cantidad: {}".format(producto.cantidad))
    p.drawString(50, 600, "Precio: {}".format(producto.precio))
    p.drawString(50, 575, "Fecha: {}".format(producto.fecha))

    # Agregamos la información del cliente
    p.drawString(50, 525, "Cliente: {}".format(producto.cliente))
    p.drawString(50, 500, "Dirección: {}".format(producto.direccion))

    # Agregamos los totales
    p.drawString(50, 450, "Subtotal: {}".format(producto.subtotal))
    p.drawString(50, 425, "Impuesto: {}".format(producto.impuesto))
    p.drawString(50, 400, "Total: {}".format(producto.total))

    # Cerramos el objeto PDF limpiamente y terminamos la respuesta del objeto HttpResponse.
    p.showPage()
    p.save()
    return response
