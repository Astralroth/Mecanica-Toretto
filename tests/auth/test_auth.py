import pytest
from django.test.client import Client
from django.contrib.auth.models import User

class AuthClass:
    
    def setup_method(self):
        print("Setting up test environment")
        
        # Create a test user
        user = User.objects.create_user(username="testuser", password="12345")
        return user
    
    @pytest.mark.django_db
    def test_can_login(self, client: Client):
        response = client.login(username="testuser", password="12345")
        assert response

    @pytest.mark.django_db
    def test_can_logout(self, client: Client):
        self.test_can_login(client)
        # User can logout
        response = client.post("/auth/logout")

        # User is redirected to login page
        assert response.status_code == 302