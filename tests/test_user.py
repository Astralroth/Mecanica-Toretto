import pytest
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Taller_mecanico.settings')
django.setup()
# from django.contrib import messages
from django.contrib.auth import get_user_model
from django.test import Client
from user.models import *
# from user.models import initialize_database

@pytest.mark.django_db
def test_user_creation():
    usuario = User.objects.create_user(
                email = 'ameliaCo@gmail.com',
                password ='Asdasd123',
                name = 'Amelia1',
                last_name = 'User',
                telefono ='74123698',
                is_staff=False
    )
    assert usuario.email == 'ameliaCo@gmail.com'

@pytest.mark.django_db
def test_super_creation():
    usuario = User.objects.create_superuser(
                email = 'userr@gmail.com',
                password ='Admin123456',
                name = 'Admin',
                last_name = 'Doce',
                telefono ='96321478'
    )
    assert usuario.is_superuser

@pytest.mark.django_db
def test_staff_user_creation():
    usuario = User.objects.create_user(
                email = 'user1@gmail.com',
                password ='Usuario123',
                name = 'User1',
                last_name = 'Local',
                telefono ='96321478',
                is_staff=True
    )
    assert usuario.is_staff

@pytest.mark.django_db
def test_super_creation_fail():
    with pytest.raises(Exception):
        User.objects.create_superuser(
            password ='Admin123456'
        )

@pytest.mark.django_db
def test_user_creation_fail():
    with pytest.raises(Exception):
        User.objects.create_user(
            password ='Admin123456'
        )


