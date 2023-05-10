"""mecanica URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import HttpResponseRedirect
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from producto import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('order/', include("pedido.urls")),
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/logout', LogoutView.as_view(), name="logout"),
    path('', lambda request: HttpResponseRedirect('auth/login')),
    path('prod/', include("producto.urls")),
    path('serv/', include("servicio.urls")),
    path('factura/<int:producto_id>/', views.generar_factura, name='generar_factura'),
]


