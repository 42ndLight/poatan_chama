from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Chama

User = get_user_model()

class ChamaTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="adminpass")
        self.member = User.objects.create_user(username="member", password="memberpass")

        self.chama = Chama.objects.create(
            chama_name="Test Chama",
            description="A test savings group",
            chama_admin=self.admin,
            cash_pool=1000.00
        )

        self.create_chama_url = reverse('chama-register')
        self.join_chama_url = reverse('chama-join')
        self.chama_detail_url = reverse('chama-detail', args=[self.chama.id])

    def test_create_chama(self):
        """Test creating a chama"""
        self.client.login(username="admin", password="adminpass")
        data = {
            "chama_name": "New Chama",
            "description": "A new group",
            "chama_admin": self.admin.id
        }
        response = self.client.post(self.create_chama_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_join_chama(self):
        """Test user joining a chama"""
        self.client.login(username="member", password="memberpass")
        data = {"chama_id": self.chama.id}
        response = self.client.post(self.join_chama_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_chama_details(self):
        """Test retrieving chama details"""
        self.client.login(username="admin", password="adminpass")
        response = self.client.get(self.chama_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["chama_name"], "Test Chama")

    def test_cash_pool_balance(self):
        """Test cash pool balance"""
        self.assertEqual(self.chama.cash_pool, 1000.00)
