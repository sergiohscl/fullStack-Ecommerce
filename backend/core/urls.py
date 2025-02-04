from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from apps.products.api.viewsets import ProductAPIView
from apps.products.api.viewsets import ProductDetailAPIView
from apps.products.api.viewsets import ProductFilterListAPIView
from apps.shop_cart.api.viewsets import ShopCartAPIView
from apps.shop_cart.api.viewsets import RemoveShortCartByNameAPIView
from apps.shop_cart.api.viewsets import AddItemShotCartAPIView
from apps.shop_cart.api.viewsets import RemoveShortCartAPIView
from core import settings
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from apps.accounts.api.viewsets import RegisterAPIView
from apps.accounts.api.viewsets import LoginAPIView
from apps.accounts.api.viewsets import LogoutAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="CART_API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0),name='schema-json'), # noqa E501
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # noqa E501
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # noqa E501

    path('admin/', admin.site.urls),
    # accounts
    path('api/v1/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/v1/register/', RegisterAPIView.as_view(), name='register'),
    path('api/v1/login/', LoginAPIView.as_view(), name='login'),
    path('api/v1/logout/', LogoutAPIView.as_view(), name='logout'),
    # products
    path('api/v1/products/', ProductAPIView.as_view(), name='products'),
    path('api/v1/products/filter-list/', ProductFilterListAPIView.as_view(), name='produtos-filter-list'), # noqa E501
    path('api/v1/products/<str:id>/', ProductDetailAPIView.as_view(), name='produto-detail'), # noqa E501
    # shop_cart
    path('api/v1/shop-cart/', ShopCartAPIView.as_view(), name='carrinho-compra'), # noqa E501
    path('api/v1/shop-cart/add-item/<str:product_id>/<int:amount>/', AddItemShotCartAPIView.as_view(), name='adicionar-item'), # noqa E501
    path('api/v1/shop-cart/remove/<str:product_id>/', RemoveShortCartAPIView.as_view(), name='remove-item'), # noqa E501
    path('api/v1/shop-cart/delete/<str:product_name>/', RemoveShortCartByNameAPIView.as_view(), name='remove-item-name'), # noqa E501
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_URL
    )
