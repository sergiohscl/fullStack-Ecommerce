from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import Usuario


class ShopCartAPITestCase(APITestCase):

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_shop_cart(self):
        url = '/api/v1/shop-cart/'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('itens', response.data)
        self.assertEqual(response.data['itens'], {})
        self.assertEqual(response.data['total'], 0)
