from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'price', 'stock', 'created_at'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'title', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
