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
from selenium.webdriver.common.keys import Keys

class TestFunctionalClass:
    
    def test_selenium(self):
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)  
        driver.get("http://127.0.0.1:8000/login")
        driver.find_element(By.ID, 'id_email').send_keys("admin@gmail.com")
        driver.find_element(By.ID, 'id_password').send_keys("Admin123")
        driver.find_element(By.XPATH, '//*[@id="formularioLogin"]/div[3]/button').click()
        assert driver.find_element(By.CSS_SELECTOR, 'p').text == 'Los Torettos'
        
def test_nav_client():
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)  
    driver.get('http://127.0.0.1:8000')
    button_nav = driver.find_element(By.XPATH, '//*[@id="navbarsExample04"]/ul/li[2]/a')
    button_nav .click()
    assert driver.current_url == 'http://127.0.0.1:8000/client/'
    driver.quit()

def test_nav_calendar():
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)  
    driver.get('http://127.0.0.1:8000')
    button_nav  = driver.find_element(By.XPATH, '//*[@id="navbarsExample04"]/ul/li[3]/a')
    button_nav .click()
    assert driver.current_url == 'http://127.0.0.1:8000/calendar/'
    driver.quit()

def test_button_calend():
    # Configurar el navegador web (en este caso, utilizaremos Chrome)
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)  
    driver.get('http://127.0.0.1:8000/client')
    button_nav  = driver.find_element(By.XPATH, '/html/body/div[2]/table/tbody/tr/th[1]/div')
    button_nav .click()
    assert driver.current_url == 'http://127.0.0.1:8000/calendar/'
    driver.quit()

def test_button_see_calend():
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(20)  
    driver.get('http://127.0.0.1:8000/client')
    button_nav  = driver.find_element(By.XPATH, '/html/body/div[2]/table/tbody/tr/th[2]/div/a')
    button_nav .click()
    assert driver.current_url == 'http://127.0.0.1:8000/running-event-list/'
    driver.quit()
