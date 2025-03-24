from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123"
        )
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.profile_url = reverse('profile')

    def test_user_registration(self):
        """Test user registration"""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        """Test user login"""
        data = {
            "username": "testuser",
            "password": "securepassword123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # Ensure token is returned

    def test_profile_retrieval(self):
        """Test retrieving user profile"""
        self.client.login(username="testuser", password="securepassword123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
    
    def test_password_change(self):
        """Test changing password"""
        self.client.login(username="testuser", password="securepassword123")
        change_password_url = reverse('change-password')
        data = {
            "old_password": "securepassword123",
            "new_password": "newsecurepassword456"
        }
        response = self.client.put(change_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        """Test deleting user account"""
        self.client.login(username="testuser", password="securepassword123")
        delete_url = reverse('delete')
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
