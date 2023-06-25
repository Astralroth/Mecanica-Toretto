import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Taller_mecanico.settings')
django.setup()
import pytest
from user.models import *
from django.contrib.auth import get_user_model
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test.client import Client
from selenium.webdriver.edge.options import Options


#Casos de pruebas
# Registro de clientes 
# No enviar campos vacios
# Alerta de usuario creado
# Visualizar PERFIL cliente
# Eliminar usuario empleado
# Confirma antes de eliminar

class TestFunctionalClass:
    
    def test_selenium(self):
        
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)  
        driver.get("http://127.0.0.1:8000/login")
        driver.find_element(By.ID, 'id_email').send_keys("admin@gmail.com")
        driver.find_element(By.ID, 'id_password').send_keys("Admin123")
        driver.find_element(By.XPATH, '//*[@id="formularioLogin"]/div[3]/button').click()
        driver.find_element(By.CSS_SELECTOR, 'p').text == 'Los Torettos'

        driver.find_element(By.XPATH, '//*[@id="empleado"]').click()
        driver.current_url == 'http://127.0.0.1:8000/employee/'

        driver.find_element(By.XPATH, '/html/body/div/table/tbody/tr/td[1]/a').click()

        assert driver.current_url == 'http://127.0.0.1:8000/running-event-list/'

class TestFunctional:
    
    def test_selenium(self):
        
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)  
        driver.get("http://127.0.0.1:8000/login")
        driver.find_element(By.ID, 'id_email').send_keys("admin@gmail.com")
        driver.find_element(By.ID, 'id_password').send_keys("Admin123")
        driver.find_element(By.XPATH, '//*[@id="formularioLogin"]/div[3]/button').click()
        driver.find_element(By.CSS_SELECTOR, 'p').text == 'Los Torettos'

        driver.find_element(By.XPATH, '//*[@id="empleado"]').click()
        driver.current_url == 'http://127.0.0.1:8000/employee/'

        driver.find_element(By.XPATH, '/html/body/div/table/tbody/tr/td[3]/a').click()

        assert driver.current_url == 'http://127.0.0.1:8000/viewOrden/'

class TestFunctionalOrden:
    
    def test_selenium(self):
        
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)  
        driver.get("http://127.0.0.1:8000/login")
        driver.find_element(By.ID, 'id_email').send_keys("admin@gmail.com")
        driver.find_element(By.ID, 'id_password').send_keys("Admin123")
        driver.find_element(By.XPATH, '//*[@id="formularioLogin"]/div[3]/button').click()
        driver.find_element(By.CSS_SELECTOR, 'p').text == 'Los Torettos'

        driver.find_element(By.XPATH, '//*[@id="empleado"]').click()
        driver.current_url == 'http://127.0.0.1:8000/employee/'

        driver.find_element(By.XPATH, '/html/body/div/table/tbody/tr/td[3]/a').click()
        driver.current_url == 'http://127.0.0.1:8000/viewOrden/'
        driver.find_element(By.XPATH, '/html/body/div/div[2]/form/center/div/button').click()

        assert driver.current_url == 'http://127.0.0.1:8000/viewOrden/'

