from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=70, verbose_name="Nome")
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(
        blank=True, null=True, verbose_name="Descrição"
    )
    price = models.FloatField(verbose_name="Preço")
    stock = models.IntegerField(verbose_name="Estoque")
    cover = models.URLField(
        blank=True, null=True, verbose_name="Imagem do Produto"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Criado em"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['name']

    def __str__(self):
        return f"Produto: {self.name}"
