from django.urls import path

from pedido.views import OrderCreateView, OrderListView


urlpatterns = [
    path('list', OrderListView.as_view(), name="listOrder"),
    path('add', OrderCreateView.as_view(), name="addOrder"),
]
