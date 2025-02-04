from django.db import models
from apps.products.models import Product
from apps.shop_cart.models import ShopCart


class ShopCartManager(models.Manager):

    def create_cart(self, customer):
        cart, created = ShopCart.objects.get_or_create(
            customer=customer,
            status=ShopCart.StatusShopCart.ATIVO,
            defaults={"itens": {}, "total": 0}
        )
        return cart

    def get_cart_ativo(self, customer):

        return ShopCart.objects.filter(
            customer=customer,
            status=ShopCart.StatusShopCart.ATIVO
        ).first()

    def add_item_shop_cart(self, shop_cart, product, amount):

        itens = shop_cart.itens

        if product.stock < amount:
            raise ValueError(
                f"Estoque insuficiente para o produto '{product.name}"
            )

        if str(product.id) in itens:
            itens[str(product.id)]['amount'] += amount
            itens[str(product.id)]['subtotal'] = itens[str(product.id)]['amount'] * product.price # noqa E501
        else:
            itens[str(product.id)] = {
                'id': product.id,
                'name': product.name,
                'title': product.title,
                'price': product.price,
                'amount': amount,
                'cover': product.cover,
                'subtotal': amount * product.price,
            }

        product.stock -= amount
        product.save()

        shop_cart.itens = itens
        shop_cart.total = sum(item['subtotal'] for item in itens.values())
        print('adicionei', shop_cart)
        shop_cart.save()
        return shop_cart

    def remove_short_cart(self, shop_cart, product_id, amount):
        itens = shop_cart.itens

        if str(product_id) not in itens:
            raise ValueError(
                f"Produto '{product_id}' não encontrado no carrinho."
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValueError("Produto não encontrado no banco de dados.")

        amount_removed = min(amount, itens[str(product_id)]['amount'])
        product.stock += amount_removed
        product.save()

        itens[str(product_id)]['amount'] -= amount_removed
        itens[str(product_id)]['subtotal'] = itens[str(product_id)]['amount'] * product.price # noqa E501

        if itens[str(product_id)]['amount'] <= 0:
            del itens[str(product_id)]

        shop_cart.itens = itens
        shop_cart.total = sum(item['subtotal'] for item in itens.values())
        shop_cart.save()
        return shop_cart
