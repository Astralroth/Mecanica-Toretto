from django.urls import path

from pedido.views import OrderCreateView, OrderListAllView, OrderListOneView


urlpatterns = [
    path('list', OrderListAllView.as_view(), name="listOrder"),
    path('list/<int:pk>', OrderListOneView.as_view(), name="listOrder"),
    path('add', OrderCreateView.as_view(), name="addOrder"),
]
