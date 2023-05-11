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

    