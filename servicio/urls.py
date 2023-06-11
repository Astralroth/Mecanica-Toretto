from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.ServicioListView.as_view(), name='listar_servicios'),
    path('registrar/', views.ServicioCreateView.as_view(), name='registrar_servicio'),
    path('modificar/<int:pk>/', views.ServicioUpdateView.as_view(), name='modificar_servicio'),
    path('eliminar/<int:pk>/', views.ServicioDeleteView.as_view(), name='eliminar_servicio'),
    path('payment/', views.ServicePaymentView.as_view(), name='pago_servicio'),
]
