from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from apps.accounts.models import Usuario
from apps.products.models import Product


class BaseTestCase(TestCase):
    def setUp(self):
        self.email = "samu@example.com"
        self.name = "samu"
        self.password = "Django13$"
        self.user = Usuario.objects.create_user(
            username=self.name,
            email=self.email,
            password=self.password,
            is_staff=True
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class ProductAPIViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('products')
        self.product_data = {
            'name': 'Produto Teste',
            'title': 'Título Teste',
            'description': 'Descrição do produto teste',
            'price': 100.0,
            'stock': 10,
            'cover': 'https://example.com/imagem.jpg'
        }

    def test_get_products(self):
        Product.objects.create(**self.product_data)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_product(self):
        response = self.client.post(self.url, self.product_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.product_data['name'])
        self.assertEqual(response.data['title'], self.product_data['title'])

    def test_create_product_without_permission(self):
        self.user.is_staff = False
        self.user.save()

        response = self.client.post(self.url, self.product_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data['detail'],
            'Apenas administradores podem cadastrar produtos.'
        )

    def test_create_product_with_invalid_data(self):
        invalid_data = self.product_data.copy()
        invalid_data['price'] = -10.0

        response = self.client.post(self.url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['error'],
            'O preço do produto deve ser maior que zero.'
        )

    def test_create_product_duplicate(self):
        Product.objects.create(**self.product_data)

        response = self.client.post(self.url, self.product_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Produto já cadastrado.')


class ProductDetailAPIViewTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.product = Product.objects.create(
            id='1',
            name='Produto Teste',
            title='Título Teste',
            description='Descrição do produto',
            price=100.0,
            stock=10,
            cover='https://example.com/imagem.jpg'
        )
        # self.url = reverse('products', kwargs={'id': self.product.id})
        self.url = f"/api/v1/products/{self.product.id}/"

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_get_product_not_found(self):
        url = "/api/v1/products/999/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Produto não encontrado.')

    def test_put_product(self):
        updated_data = {
            'name': 'Produto Atualizado',
            'title': 'Título Atualizado',
            'description': 'Descrição atualizada.',
            'price': 120.0,
            'stock': 15,
            'cover': 'https://example.com/updated_imagem.jpg'
        }

        response = self.client.put(self.url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        self.assertEqual(response.data['price'], updated_data['price'])

    def test_delete_product(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(
            Product.DoesNotExist, Product.objects.get, id=self.product.id
        )

    def test_delete_product_not_found(self):
        url = "/api/v1/products/999/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Produto não encontrado.')
