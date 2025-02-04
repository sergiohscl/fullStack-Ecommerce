from django.test import TestCase
from apps.accounts.models import Usuario
from apps.shop_cart.models import ShopCart


class ShopCartTestCase(TestCase):

    def setUp(self):
        self.user = Usuario.objects.create_user(
            username='cliente_test',
            password='senha123',
            email='cliente@test.com'
        )
        self.cart = ShopCart.objects.create(
            customer=self.user,
            itens={
                '1': {
                    'name': 'Produto A',
                    'title': 'Produto A',
                    'price': 10.0,
                    'amount': 2,
                    'cover': 'url_a'
                },
                '2': {
                    'name': 'Produto B',
                    'title': 'Produto B',
                    'price': 15.0,
                    'amount': 1,
                    'cover': 'url_b'
                }
            },
            total=35.0,
            status=ShopCart.StatusShopCart.ATIVO
        )

    def test_shop_cart_creation(self):
        self.assertEqual(self.cart.customer.username, 'cliente_test')
        self.assertEqual(self.cart.itens['1']['name'], 'Produto A')
        self.assertEqual(self.cart.total, 35.0)
        self.assertEqual(self.cart.status, ShopCart.StatusShopCart.ATIVO)

    def test_shop_cart_status_update(self):
        self.cart.status = ShopCart.StatusShopCart.FINALIZADO
        self.cart.save()
        self.assertEqual(self.cart.status, ShopCart.StatusShopCart.FINALIZADO)

    def test_cart_items_field(self):
        self.assertIn('1', self.cart.itens)
        self.assertEqual(self.cart.itens['1']['amount'], 2)

    def test_cart_total_calculation(self):
        total_calculated = sum(
            item['price'] * item['amount'] for item in self.cart.itens.values()
        )
        self.assertEqual(self.cart.total, total_calculated)

    def test_str_method(self):
        self.assertEqual(
            str(
                self.cart
            ),
            f"Carrinho de compra {self.cart.id} do cliente {self.cart.customer.username}" # noqa E501
        )

    def test_shop_cart_association_with_user(self):
        self.assertEqual(self.user.shop_cart.count(), 1)
