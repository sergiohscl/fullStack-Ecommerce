from django.test import TestCase
from apps.products.models import Product


class ProductModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Produto Exemplo",
            title="Título Exemplo",
            description="Descrição do produto.",
            price=99.99,
            stock=10,
            cover="https://link.da.imagem/produto.jpg"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Produto Exemplo")
        self.assertEqual(self.product.title, "Título Exemplo")
        self.assertEqual(self.product.description, "Descrição do produto.")
        self.assertEqual(self.product.price, 99.99)
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(
            self.product.cover, "https://link.da.imagem/produto.jpg")

    def test_str_method(self):
        self.assertEqual(str(self.product), "Produto: Produto Exemplo")

    def test_product_ordering(self):
        product1 = Product.objects.create(
            name="Produto B", title="Título B", price=49.99, stock=5
        )
        product2 = Product.objects.create(
            name="Produto A", title="Título A", price=29.99, stock=2
        )
        products = Product.objects.all()
        self.assertEqual(products[0], product2)
        self.assertEqual(products[1], product1)

    def test_product_fields(self):
        self.assertTrue(hasattr(self.product, 'name'))
        self.assertTrue(hasattr(self.product, 'title'))
        self.assertTrue(hasattr(self.product, 'price'))
        self.assertTrue(hasattr(self.product, 'stock'))
        self.assertTrue(hasattr(self.product, 'cover'))
