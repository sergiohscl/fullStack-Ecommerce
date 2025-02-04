from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.products.api.serializers import ProductSerializer
from apps.products.managers.product_manager import ProductManager
from apps.products.models import Product


class ProductAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post']

    def get_permissions(self):
        """
        Define permissões específicas para cada método HTTP.
        """
        if self.request.method == "GET":
            return []
        return [IsAuthenticated()]

    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)},
        operation_summary="Busca todos os produtos com paginação.",
    )
    def get(self, request):
        products = Product.objects.all()

        # Configuração da paginação
        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)

        # Serializa os produtos paginados
        serializer = ProductSerializer(paginated_products, many=True)

        # Retorna a resposta paginada
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        responses={201: ProductSerializer(many=False)},
        request_body=ProductSerializer,
        operation_summary="Cadastra produtos",
    )
    def post(self, request):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem cadastrar produtos."
            )

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Verifica se o produto já existe
            name = serializer.validated_data.get("name")
            title = serializer.validated_data.get("title")

            if Product.objects.filter(name=name, title=title).exists():
                return Response(
                    {"detail": "Produto já cadastrado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Instancia o ProductManager e cria o produto
            manager = ProductManager()
            manager.model = Product
            product = manager.create_product(**serializer.validated_data)

            response_serializer = ProductSerializer(product)
            return Response(
                response_serializer.data, status=status.HTTP_201_CREATED
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


class ProductDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    http_method_names = ['get', 'put', 'delete']

    def get_permissions(self):
        """
        Define permissões específicas para cada método HTTP.
        """
        if self.request.method == "GET":
            return []
        return [IsAuthenticated()]

    @swagger_auto_schema(
        responses={200: ProductSerializer(many=False)},
        operation_summary="Busca único produto.",
    )
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        if not product_id:
            return Response(
                {'detail': 'ID do produto não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response(
                {'detail': 'Produto não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={200: ProductSerializer(many=False)},
        operation_summary="Atualiza produto.",
    )
    def put(self, request, *args, **kwargs):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem atualizar produtos."
            )

        product_id = kwargs.get('id')
        if not product_id:
            return Response(
                {'detail': 'ID do produto não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            manager = ProductManager()
            product = manager.update_product(
                Product, product_id, request.data
            )

            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response(
                {'detail': 'Produto não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        responses={204: 'Produto deletado com sucesso.'},
        operation_summary="Exclui produto.",
    )
    def delete(self, request, *args, **kwargs):
        # Verifica se o usuário logado é administrador
        if not request.user.is_staff:
            raise PermissionDenied(
                "Apenas administradores podem deletar produtos."
            )

        product_id = kwargs.get('id')
        if not product_id:
            return Response(
                {'detail': 'ID do produto não fornecido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            manager = ProductManager()
            manager.delete_product(Product, product_id)
            return Response(
                {'detail': 'Produto deletado com sucesso.'},
                status=status.HTTP_204_NO_CONTENT
            )

        except Product.DoesNotExist:
            return Response(
                {'detail': 'Produto não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProductFilterListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ['exact'],
        'name': ['icontains', ],
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_QUERY,
                description="ID do produto",
                type=openapi.TYPE_STRING
            ),
        ],
        operation_summary="lista produto por ID ou nome.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
