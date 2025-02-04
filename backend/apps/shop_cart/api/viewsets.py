from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.accounts.models import Usuario
from apps.products.models import Product
from apps.shop_cart.api.serializers import ShopCartSerializer
from apps.shop_cart.managers.shop_cart_manager import ShopCartManager


class ShopCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopCartSerializer
    http_method_names = ['post', 'get']

    @swagger_auto_schema(
        responses={200: ShopCartSerializer(many=True)},
    )
    def get(self, request):
        try:
            customer = request.user
            manager = ShopCartManager()
            shot_cart = manager.get_cart_ativo(
                customer=customer
            )

            if not shot_cart:
                return Response(
                    {"detail": "Nenhum carrinho ativo encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )

            serializer = self.serializer_class(shot_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response(
                {"detail": "Cliente não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"Erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        responses={201: ShopCartSerializer(many=False)},
        request_body=ShopCartSerializer,
        operation_summary="Cria carrinho de compra.",
    )
    def post(self, request):
        try:
            customer = request.user
            manager = ShopCartManager()
            short_cart = manager.create_cart(
                customer=customer
            )

            serializer = ShopCartSerializer(short_cart)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AddItemShotCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopCartSerializer
    http_method_names = ['post',]

    @swagger_auto_schema(
        responses={201: ShopCartSerializer(many=False)},
        operation_summary="Adiciona Item ao carrinho de compra.",
    )
    def post(self, request, product_id, amount):
        try:
            manager = ShopCartManager()

            # Obtém o carrinho ativo
            shop_cart = manager.get_cart_ativo(request.user)
            if not shop_cart:
                return Response(
                    {'detail': 'Carrinho de compras ativo não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Verifica se o produto existe
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {'detail': 'Produto não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Adiciona o produto ao carrinho
            try:
                shop_cart = manager.add_item_shop_cart(
                    shop_cart, product, amount
                )

            except ValueError as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    'detail': 'Produto adicionado ao carrinho com sucesso.',
                    'shop_cart': {
                        'id': shop_cart.id,
                        'itens': shop_cart.itens,
                        'total': shop_cart.total
                    }
                },
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RemoveShortCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopCartSerializer
    http_method_names = ['delete',]

    @swagger_auto_schema(
        responses={200: "Item removido e atualizado no carrinho com sucesso."},
        operation_description="Remove um item do carrinho, decrementa sua quantidade e atualiza o estoque do produto.", # noqa E501
        operation_summary="Remove Item do carrinho de compra.",
    )
    def delete(self, request, product_id=None, amount=1):
        try:
            manager = ShopCartManager()

            # Obtém o carrinho ativo
            shop_cart = manager.get_cart_ativo(request.user)

            if not shop_cart:
                return Response(
                    {'detail': 'Carrinho de compras ativo não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                shop_cart = manager.remove_short_cart(
                    shop_cart, product_id, amount
                )
            except ValueError as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {"detail": "Item removido e atualizado no carrinho com sucesso."}, # noqa E501
                status=status.HTTP_204_NO_CONTENT
            )

        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RemoveShortCartByNameAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopCartSerializer
    http_method_names = ['delete']

    @swagger_auto_schema(
        responses={200: "Item removido e atualizado no carrinho com sucesso."},
        operation_description="Remove um item do carrinho pelo nome do produto, decrementa sua quantidade e atualiza o estoque do produto.", # noqa E501
        operation_summary="Remove Item do carrinho de compra pelo nome.",
    )
    def delete(self, request, product_name=None, amount=1):
        try:
            manager = ShopCartManager()

            # Obtém o carrinho ativo
            shop_cart = manager.get_cart_ativo(request.user)

            if not shop_cart:
                return Response(
                    {'detail': 'Carrinho de compras ativo não encontrado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Produto não encontrado no banco de dados."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                shop_cart = manager.remove_short_cart(
                    shop_cart, product.id, amount
                )
            except ValueError as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {"detail": "Item removido e atualizado no carrinho com sucesso."}, # noqa E501
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return Response(
                {"detail": f"Erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
