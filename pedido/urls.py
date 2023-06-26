from django.urls import path

from pedido.views import OrderCreateView, OrderListAllView, OrderListOneView


urlpatterns = [
    path('list', OrderListAllView.as_view(), name="listOrder"),
    path('list/det', OrderListOneView.as_view(), name="listOneOrder"),
    path('add', OrderCreateView.as_view(), name="addOrder"),
]
