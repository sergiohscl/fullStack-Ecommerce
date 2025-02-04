from django.db import models

from apps.products.models import Product


class ProductManager(models.Manager):

    def create_product(self, name, title, description, price, stock, cover):

        if price <= 0:
            raise ValueError("O preço do produto deve ser maior que zero.")
        if stock < 0:
            raise ValueError("O estoque não pode ser negativo.")

        product = self.create(
            name=name,
            title=title,
            description=description,
            price=price,
            stock=stock,
            cover=cover
        )
        return product

    def get_by_uuid(self, model, product_id):

        if not product_id:
            raise ValueError("O ID do produto é obrigatório.")

        try:
            return model.objects.get(id=product_id)
        except model.DoesNotExist:
            raise model.DoesNotExist("Produto não encontrado.")

    def update_product(self, model, product_id, data):
        try:
            product = self.get_by_uuid(model, product_id)
        except Product.DoesNotExist:
            raise ValueError("Produto não encontrado.")

        if "price" in data and data["price"] <= 0:
            raise ValueError("O preço do produto deve ser maior que zero.")
        if "stock" in data and data["stock"] < 0:
            raise ValueError("O estoque não pode ser negativo.")

        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    def delete_product(self, model, product_id):
        try:
            product = self.get_by_uuid(model, product_id)
            product.delete()
            return True
        except Product.DoesNotExist:
            raise ValueError("Produto não encontrado.")
