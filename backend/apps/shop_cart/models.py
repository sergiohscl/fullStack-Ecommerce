from django.db import models
from apps.accounts.models import Usuario


class ShopCart(models.Model):
    class StatusShopCart(models.TextChoices):
        ATIVO = 'A', 'Ativo'
        FINALIZADO = 'F', 'Finalizado'

    customer = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='shop_cart'
    )
    itens = models.JSONField(
        default=dict,
        help_text="Estrutura: {'product_id': {'name': str, 'title': str, 'price': float, 'amount': int, 'cover': str}}" # noqa E501
    )
    total = models.FloatField(blank=True, null=True)
    status = models.CharField(
        max_length=1,
        choices=StatusShopCart.choices,
        default=StatusShopCart.ATIVO
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = 'Carrinho de Compra'
        verbose_name_plural = 'Carrinhos de Compras'

    def __str__(self):
        return f"Carrinho de compra {self.id} do cliente {self.customer.username}" # noqa E501
