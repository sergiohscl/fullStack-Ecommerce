from django.contrib import admin
from .models import ShopCart


@admin.register(ShopCart)
class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('customer__username', 'customer__email')
    readonly_fields = ('total', 'created_at', 'updated_at')
    fieldsets = (
        ('Informações do Cliente', {
            'fields': ('customer',)
        }),
        ('Detalhes do Carrinho', {
            'fields': ('itens', 'total', 'status')
        }),
    )
    ordering = ('-id',)

    def has_add_permission(self, request):
        """Impede a criação de carrinhos diretamente no admin."""
        return False
