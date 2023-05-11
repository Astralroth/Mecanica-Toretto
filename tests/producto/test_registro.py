import pytest
from django.test.client import Client

from producto.models import Product

from ..auth.test_auth import AuthClass
from django.contrib.auth.models import User

# Create your test here.
class TestRegistroClass(AuthClass):

    def setup_method(self):
        print('Setting up test enviroment')
        super().setup_method()
        #Create a Test Product Register
        Product = Product.objects.create(name = "Motor de 9 Cilindros")

    @pytest.fixture(scope='function', autouse=True)
    def login(self, client: Client):
        self.test_can_login(client)

    @pytest.mark.django_db
    def test_can_create_register(self, client:Client):
        #User can create a new register
        response = client.post("product/add", {"action" : "addProduct", "data": '[{"nombre"}:{"Testeo"}, [{"precio"}:{"120000"},[{"estado"}:{"nuevo"}]]]'})
        assert response.status_code == 200
    
    #Create a wrong register 
    @pytest.mark.django_db
    def test_can_create_register_wrong(self, client:Client):
        #User can create a new register
        response = client.post("product/add", {"action" : "addProduct", "data": '[{"nombre"}:{"Testeo"}, [{"precio"}:{"120000"},[{"estado"}:{""}]]]'})
        assert response.status_code == 200
        #validate if the response is a error, test will fail
        assert response.json()['status'] == 'ERROR'
        #validate if the response is correct
        assert response.json()['message'] == 'El estado del producto no puede estar nulo'

    #Create a test to view if a user can edit a register
    @pytest.mark.django_bd
    def test_can_edit_register(self, client:Client):
        #User can create a new register
        response = client.post("product/add", {"action" : "addProduct", "data": '[{"nombre"}:{"Testeo"}, [{"precio"}:{"120000"},[{"estado"}:{"nuevo"}]]]'})
        assert response.status_code == 200
        #User can edit a register
        response = client.post("product/list", {"action" : "edit", "data": '[{"nombre"}:{"Testeo"}, [{"precio"}:{"250000"},[{"estado"}:{"De fabrica"}]]]'})
        assert response.status_code == 200
        #validate if the response is not an error 
        #if the response is an error, tets will fail
        assert response.json()['status'] == 'CORRECT'
        #confirm the register has been edited 
        response = client.post("/product/list", {"action":"getData"})
        print(response.json())
        assert response.json(['data'][0]['json'] == [{'nombre':'Motor de 8 Cilindros', 'precio':'250000', 'estado':'De fabrica'}])

    #Create a test to check if the user can write 100 words in the register name
    @pytest.mark.django_db 
    def test_can_write_70_words_in_order_name(self, client: Client):
        

        name = 't'*100

        #user can create a new register 
        response = client.post("/product/add", {"action" : "addProduct", "data": '[{"nombre"}:{"'+name+'"}, [{"nombre":"test"},{"precio"}:{"120000"},[{"estado"}:{"nuevo"}]]]'})
        assert response.status_code == 200
        #validate if the response is an error, the test will fail
        assert response.json()['status'] == 'ERROR'
        #Validate the response messege is correct
        assert response.json()['message'] == 'El nombre del pedido no puede ser mayor a 50 caracteres'

        