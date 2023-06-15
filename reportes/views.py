from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, JsonResponse
from django.db import models
from core.models import Boleta
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Create your views here.
@method_decorator(
    [csrf_exempt, login_required(redirect_field_name="listOrder", login_url="login")],
    name="dispatch",
)
class SalesView(TemplateView):
    template_name = "reportes/ventas.html"

    def post(self, request: HttpRequest):
        action = request.POST["action"]
        if action == "search_sales":
            init_date = request.POST.get("init_date", "")
            end_date = request.POST.get("end_date", "")
            productos = Boleta.objects.filter(fecha__range=[init_date, end_date])
            parsed: dict = serialize("json", productos)
            json_v = json.loads(parsed)
            
            data = []
            for i in range(0, productos.__len__()):
                json_v[i]["fields"]["id"] = json_v[i]["pk"]
                data.append(json_v[i]["fields"])

            response = {"data": data}
            return JsonResponse(response, safe=False)
        else:
            return JsonResponse({"error": "No se ha encontrado la acción solicitada"})