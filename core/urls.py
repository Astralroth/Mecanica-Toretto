from django.urls import path, include
from .views import IndexView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', IndexView.as_view(), name='index' ),
    path('order/', include("pedido.urls")),
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/logout', LogoutView.as_view(), name="logout"),
    path('prod/', include("producto.urls")),
    path('serv/', include("servicio.urls")),
    path('sales/', include("reportes.urls")),
]