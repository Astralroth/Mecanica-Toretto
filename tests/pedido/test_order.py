import pytest
from django.test.client import Client

from pedido.models import Product

from ..auth.test_auth import TestAuthClass
from django.contrib.auth.models import User

# Create your tests here.
class TestOrderClass(TestAuthClass):
    
    def setup_method(self):
        print("Setting up test environment")
        super().setup_method()
        # Create a test products
        products = Product.objects.create(name="Aceite para Motor")

    @pytest.mark.django_db
    def test_can_create_order(self, client: Client):
        self.test_can_login(client)
        # User can create a new order
        response = client.post("/order/add", {"action":"addOrder", "data": '[{"name":"test"}, [{"name":"Aceite para Motor", "quantity":1}]]'})
        assert response.status_code == 200
    
    # create a test to create a order wrong
    @pytest.mark.django_db
    def test_can_create_order_wrong(self, client: Client):
        self.test_can_login(client)
        # User can create a new order
        response = client.post("/order/add", {"action":"addOrder", "data": '[{"name":"test"}, [{"name":"Aceite para Motor", "quantity":-1}]]'})
        assert response.status_code == 200
        # validate the response is an error
        # * if the response is not an error, the test will fail
        assert response.json()['status'] == 'Error'
        # validate the response message is correct
        assert response.json()['message'] == 'La cantidad de productos no puede ser negativa'

    # create a test to check if the user can edit an order
    @pytest.mark.django_db
    def test_can_edit_order(self, client: Client):
        self.test_can_login(client)
        # User can create a new order
        response = client.post("/order/add", {"action":"addOrder", "data": '[{"name":"test"}, [{"name":"Aceite para Motor", "quantity":1}]]'})
        assert response.status_code == 200
        # User can edit an order
        response = client.post("/order/list", {"action":"edit", "data": '[{"name":"test", "value":1}, [{"name":"Aceite para Motor", "quantity":2}]]'})
        assert response.status_code == 200
        # validate the response is not an error
        # * if the response is an error, the test will fail
        assert response.json()['status'] == 'Correct'
        # Confirm that the order was edited
        response = client.post("/order/list", {"action":"getData"})
        print(response.json())
        assert response.json()['data'][0]['json'] == [{'name':'Aceite para Motor', 'quantity':2}]
    
    # create a test to check if the user can write 100 words in the order name
    @pytest.mark.django_db
    def test_can_write_100_words_in_order_name(self, client: Client):
        self.test_can_login(client)
        
        name = 'a'*100
        
        # User can create a new order
        response = client.post("/order/add", {"action":"addOrder", "data": '[{"name":"'+name+'"}, [{"name":"Aceite para Motor", "quantity":1}]]'})
        assert response.status_code == 200
        # validate the response is an error
        # * if the response is not an error, the test will fail
        assert response.json()['status'] == 'Error'
        # validate the response message is correct
        assert response.json()['message'] == 'El nombre del pedido no puede ser mayor a 50 caracteres'
        
    # create a tes to check if the user can order more than 20 quantities of a product
    @pytest.mark.django_db
    def test_can_order_more_than_20_quantities_of_a_product(self, client: Client):
        self.test_can_login(client)
        
        # User can create a new order
        response = client.post("/order/add", {"action":"addOrder", "data": '[{"name":"test"}, [{"name":"Aceite para Motor", "quantity":21}]]'})
        assert response.status_code == 200
        # validate the response is an error
        # * if the response is not an error, the test will fail
        assert response.json()['status'] == 'Error'
        # validate the response message is correct
        assert response.json()['message'] == 'La cantidad de productos no puede ser mayor a 20 unidades'
        
    # create a test to check if the user can order negative quantities of a product
    @pytest.mark.django_db
    def test_can_order_negative_quantities_of_a_product(self, client: Client):
        self.test_can_login(client)
        
        # User can create a new order
        response = client.post("/order/add", {"action":"addOrder", "data": '[{"name":"test"}, [{"name":"Aceite para Motor", "quantity":-1}]]'})
        assert response.status_code == 200
        # validate the response is an error
        # * if the response is not an error, the test will fail
        assert response.json()['status'] == 'Error'
        # validate the response message is correct
        assert response.json()['message'] == 'La cantidad de productos no puede ser negativa'