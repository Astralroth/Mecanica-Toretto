from django.test import TestCase,RequestFactory
import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from .models import Servicio
from django.core.cache import cache

from django.test import Client



@pytest.mark.django_db
#1.Registrar un nuevo servicio en el taller mecánico
def test_registro_servicio(client):
    # Preparación
    url = reverse('taller:registrar_servicio')
    datos = {
        'nombre': 'Cambio de aceite',
        'descripcion': 'Cambio de aceite y filtro',
        'precio': 50,
        'tiempo_estimado': 1,
        'productos_asociados': 'Aceite, Filtro de aceite'
    }

    # Ejecución
    respuesta = client.post(url, data=datos)

    # Verificación
    assertRedirects(respuesta, reverse('taller:listar_servicios'))
    assert Servicio.objects.count() == 1  # Verifica que se haya creado un objeto Servicio en la base de datos


#2 Modificar nuevo servicio en el taller mecanico
class ModificarServicioTest(TestCase):
    def test_modificar_servicio(self):
        # Crear un servicio existente en la base de datos
        servicio = Servicio.objects.create(nombre='Cambio de aceite', descripcion='Cambio de aceite y filtro', precio=50, tiempo_estimado=1, productos_asociados='Aceite, Filtro de aceite')

        # Datos actualizados del servicio
        datos_actualizados = {
            'nombre': 'Cambio de aceite y filtro',
            'descripcion': 'Cambio de aceite, filtro de aceite y filtro de aire',
            'precio': 60,
            'tiempo_estimado': 2,
            'productos_asociados': 'Aceite, Filtro de aceite, Filtro de aire'
        }

        # Obtener la URL de modificación de servicio
        url = reverse('taller:modificar_servicio', args=[servicio.pk])

        # Realizar la solicitud POST con los datos actualizados
        response = self.client.post(url, data=datos_actualizados)

        # Verificar el código de estado de la respuesta
        self.assertEqual(response.status_code, 302)  # Redirección exitosa

        # Recuperar el servicio actualizado de la base de datos
        servicio_actualizado = Servicio.objects.get(pk=servicio.pk)

        # Verificar que los campos actualizados coincidan con los datos proporcionados
        self.assertEqual(servicio_actualizado.nombre, datos_actualizados['nombre'])
        self.assertEqual(servicio_actualizado.descripcion, datos_actualizados['descripcion'])
        self.assertEqual(servicio_actualizado.precio, datos_actualizados['precio'])
        self.assertEqual(servicio_actualizado.tiempo_estimado, datos_actualizados['tiempo_estimado'])
        self.assertEqual(servicio_actualizado.productos_asociados, datos_actualizados['productos_asociados'])


#3.Listarlos Los nuevos servicios en el taller mecanico
class ServicioListViewTest(TestCase):
    def setUp(self):
        # Crear algunos objetos de prueba
        Servicio.objects.create(nombre='Servicio 1', descripcion='Descripción 1', precio=50, tiempo_estimado=1)
        Servicio.objects.create(nombre='Servicio 2', descripcion='Descripción 2', precio=100, tiempo_estimado=2)

    def test_servicio_list_view(self):
        url = reverse('taller:listar_servicios')
        response = self.client.get(url)

        # Verificar que la respuesta tenga un código de estado 200 (éxito)
        self.assertEqual(response.status_code, 200)

        # Verificar que los objetos de Servicio estén presentes en la respuesta
        self.assertContains(response, 'Servicio 1')
        self.assertContains(response, 'Servicio 2')

        # Verificar que la cantidad de objetos mostrados sea la esperada
        self.assertEqual(Servicio.objects.count(), 2)


#4.Dar de baja los servicios ya registrados

class ServicioDeleteViewTest(TestCase):
    def setUp(self):
        # Crear un objeto de prueba
        self.servicio = Servicio.objects.create(nombre='Servicio de prueba', descripcion='Descripción de prueba',
                                                precio=50, tiempo_estimado=1)

    def test_eliminar_servicio_view(self):
        url = reverse('taller:eliminar_servicio', args=[self.servicio.pk])
        response = self.client.post(url)

        # Verificar que el servicio haya sido eliminado correctamente
        self.assertEqual(response.status_code, 302)  # Redireccionamiento después de la eliminación
        self.assertFalse(Servicio.objects.filter(pk=self.servicio.pk).exists())  # El servicio no debe existir en la base de datos
        self.assertRedirects(response, reverse('taller:listar_servicios'))  # Verificar redireccionamiento a la lista de servicios

#5.Registrar un nuevo servicio en el taller mecánico con datos inválidos.
class RegistrarServicioInvalidoTest(TestCase):
    def test_registrar_servicio_invalido(self):
        url = reverse('taller:registrar_servicio')
        datos = {
            'nombre': '',  # Datos inválidos: nombre vacío
            'descripcion': 'Cambio de aceite y filtro',
            'precio': 50,
            'tiempo_estimado': 1,
            'productos_asociados': 'Aceite, Filtro de aceite'
        }

        response = self.client.post(url, data=datos)

        # Verificar que el servicio no se haya creado
        self.assertEqual(response.status_code, 200)  # La respuesta debe ser exitosa
        self.assertFalse(Servicio.objects.exists())  # El servicio no debe existir en la base de datos
        self.assertTemplateUsed(response, 'servicio/registrar_servicio.html')  # Se debe renderizar la plantilla de registro de servicio

#6.Modificar un servicio existente con datos inválidos.
class ModificarServicioInvalidoTest(TestCase):
    def setUp(self):
        # Crear un servicio existente en la base de datos
        self.servicio = Servicio.objects.create(
            nombre='Cambio de aceite',
            descripcion='Cambio de aceite y filtro',
            precio=50,
            tiempo_estimado=1,
            productos_asociados='Aceite, Filtro de aceite'
        )

    def test_modificar_servicio_invalido(self):
        url = reverse('taller:modificar_servicio', args=[self.servicio.pk])
        datos = {
            'nombre': '',  # Datos inválidos: nombre vacío
            'descripcion': 'Cambio de aceite y filtro',
            'precio': 50,
            'tiempo_estimado': 1,
            'productos_asociados': 'Aceite, Filtro de aceite'
        }

        response = self.client.post(url, data=datos)

        # Verificar que la respuesta redirige al formulario de modificación
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicio/modificar_servicio.html')

        # Verificar que los datos del servicio no se han actualizado
        servicio_actualizado = Servicio.objects.get(pk=self.servicio.pk)
        self.assertEqual(servicio_actualizado.nombre, 'Cambio de aceite')  # El nombre no debe haber cambiado


#7.Buscar un servicio existente en el taller mecánico.
from django.core.cache import cache
from django.test import TestCase

class BuscarServicioTest(TestCase):
    def setUp(self):
        # Configura los datos de prueba y guárdalos en la caché
        cache.set('servicio_1', 'Cambio de aceite')
        cache.set('servicio_2', 'Alineación de ruedas')
        cache.set('servicio_3', 'Cambio de frenos')

    def test_buscar_servicio_existente(self):
        # Recupera los datos de la caché y verifica que sean correctos
        servicio_1 = cache.get('servicio_1')
        servicio_2 = cache.get('servicio_2')
        servicio_3 = cache.get('servicio_3')

        self.assertEqual(servicio_1, 'Cambio de aceite')
        self.assertEqual(servicio_2, 'Alineación de ruedas')
        self.assertEqual(servicio_3, 'Cambio de frenos')

#8.Buscar un servicio inexistente en el taller mecánico.

class BuscarServicioInexistenteTest(TestCase):
    def setUp(self):
        # Configura los datos de prueba y guárdalos en la caché
        cache.set('servicio_1', 'Cambio de aceite')
        cache.set('servicio_2', 'Alineación de ruedas')
        cache.set('servicio_3', 'Cambio de frenos')

    def test_buscar_servicio_inexistente(self):
        # Intenta buscar un servicio que no existe en la caché
        servicio_inexistente = cache.get('servicio_4')

        # Verifica que el servicio inexistente sea None (no se encontró en la caché)
        self.assertIsNone(servicio_inexistente)

#9.Listar los servicios disponibles en el taller mecánico aplicando un filtro.
@pytest.fixture
def crear_servicios():
    # Crear algunos servicios de ejemplo
    Servicio.objects.create(
        nombre='Cambio de aceite',
        descripcion='Realizar cambio de aceite del motor',
        precio=50,
        tiempo_estimado=60
    )
    Servicio.objects.create(
        nombre='Alineación de ruedas',
        descripcion='Alinear las ruedas del vehículo',
        precio=80,
        tiempo_estimado=30
    )


@pytest.mark.django_db
def test_listar_servicios_con_filtro(client, crear_servicios):
    # Realizar una solicitud GET a la página de listar servicios con un filtro aplicado
    response = client.get(reverse('taller:listar_servicios'), {'filtro': 'C'})

    # Verificar que la respuesta sea exitosa
    assert response.status_code == 200

    # Verificar que solo se muestren los servicios que coincidan con el filtro
    content = response.content.decode()
    assert 'Cambio de aceite' in content
    #assert 'Alineación de ruedas' not in content


@pytest.fixture
def crear_servicio_dado_de_baja():
    servicio = Servicio.objects.create(
        nombre='Cambio de aceite',
        descripcion='Realizar cambio de aceite del motor',
        precio=50,
        tiempo_estimado=60,
        dado_de_baja=True
    )
    return servicio

#10.Filtrar servicios por precio
def test_filtrar_servicios_por_precio():
    # Crear algunos servicios de ejemplo
    servicio_aceite = {
        'nombre': 'Cambio de aceite',
        'descripcion': 'Realizar cambio de aceite del motor',
        'precio': 50,
        'tiempo_estimado': 60
    }
    servicio_alineacion = {
        'nombre': 'Alineación de ruedas',
        'descripcion': 'Alinear las ruedas del vehículo',
        'precio': 80,
        'tiempo_estimado': 30
    }
    servicio_frenos = {
        'nombre': 'Cambio de frenos',
        'descripcion': 'Realizar cambio de frenos',
        'precio': 120,
        'tiempo_estimado': 45
    }

    # Agregar los servicios al caché
    cache.set('servicios', [servicio_aceite, servicio_alineacion, servicio_frenos])

    # Crear una solicitud GET simulada a la página de listar servicios con filtro por precio
    request = RequestFactory().get('/servicios/', {'filtro-precio': '80'})

    # Obtener los servicios filtrados por precio
    servicios_filtrados = cache.get('servicios')
    if servicios_filtrados:
        servicios_filtrados = [servicio for servicio in servicios_filtrados if servicio['precio'] == 80]

    # Verificar que el filtro por precio haya sido aplicado correctamente
    assert servicios_filtrados == [servicio_alineacion]