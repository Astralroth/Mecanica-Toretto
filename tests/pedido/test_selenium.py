import pytest
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from django.test.client import Client
from selenium.webdriver.edge.options import Options

class TestFunctionalClass:
    
    def setup_method(self, client: Client):
        opt = Options()
        opt.add_argument("--headless")
        self.driver = Edge(options=opt)
        self.driver

    @pytest.fixture(scope="function", autouse=True)
    def test_login(self):
        self.driver.get("http://localhost:8000")
        self.driver.find_element(By.NAME, 'username').send_keys("astralroth")
        self.driver.find_element(By.NAME, 'password').send_keys("Franco12")
        self.driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
        self.driver.get("http://localhost:8000/order/list")
        assert self.driver.find_element(By.CSS_SELECTOR, 'h1').text == 'Mis Ordenes'
    
    #create a selenium test to edit a order
    def test_edit_order(self):
        self.driver.get("http://localhost:8000/order/list")
        self.driver.find_element(By.ID,0).click()
        self.driver.find_element(By.CSS_SELECTOR,'.sorting_1 > #\31').click()
        self.driver.find_element(By.CSS_SELECTOR,'.sorting_1 > #\31').send_keys(100)
        self.driver.find_element(By.CSS_SELECTOR, 'button[type=submit]').click()
        assert self.driver.find_element(By.CSS_SELECTOR, 'h1').text == 'Mis Ordenes'