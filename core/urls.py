from django.urls import path, include

urlpatterns = [
    path('order/', include("pedido.urls")),
    path('prod/', include("producto.urls")),
    path('serv/', include("servicio.urls")),
    path('sales/', include("reportes.urls")),
]