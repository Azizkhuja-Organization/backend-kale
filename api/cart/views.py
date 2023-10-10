from django.db.models import F, Sum, Q, Exists, OuterRef
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.cart.serializers import CartProductCreateSerializer, CartProductListSerializer
from api.paginator import CustomPagination
from api.permissions import IsClient
from common.order.models import Cart, CartProduct, Wishlist, Comparison
from common.product.models import Product


# CART

class CountersAPIView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            cartProducts = CartProduct.objects.filter(cart__user=request.user).count()
            wishlistProducts, created = Wishlist.objects.get_or_create(user=request.user)
            comparisonProducts, created = Comparison.objects.get_or_create(user=request.user)
            response = {
                'inCart': cartProducts,
                'inWishlist': wishlistProducts.products.count(),
                'inComparison': comparisonProducts.products.count(),
            }
        else:
            response = {
                'inCart': 0,
                'inWishlist': 0,
                'inComparison': 0
            }

        return Response(response, status=status.HTTP_200_OK)


class CartAddSubAPIView(APIView):
    permission_classes = [IsClient]

    def get(self, request):
        id = request.query_params.get('id')
        product = Product.objects.filter(id=id).first()
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        hasCart = False
        action = request.query_params.get('action')
        if action is not None and action in ['add', 'sub']:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cartProducts = cart.cartCartProduct.all().select_related('cart', 'product')
            cartProduct = cartProducts.filter(product=product, cart=cart).first()

            if cartProduct and product.quantity <= cartProduct.quantity:
                return Response({"message": "Product quantity does not enough"}, status=status.HTTP_400_BAD_REQUEST)

            if cartProduct is None and action == 'add':
                hasCart = True
                CartProduct.objects.create(cart=cart, product=product, orderPrice=product.amount)
            elif action == 'add' and cartProduct:
                hasCart = True
                cartProduct.add
            elif action == 'sub' and cartProduct:
                if cartProduct.quantity == 1:
                    hasCart = False
                    cartProduct.delete()
                cartProduct.sub
            quantity = 0 if cartProduct is None else cartProduct.quantity
            return Response({'hasCart': hasCart, 'quantity': quantity if hasCart else 0},
                            status=status.HTTP_200_OK)


# CART PRODUCTS

class CartProductCreateAPIView(CreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductCreateSerializer
    permission_classes = [IsClient]


class CartProductListAPIView(ListAPIView):
    queryset = CartProduct.objects.select_related('cart', 'cart__user', 'product').all()
    serializer_class = CartProductListSerializer
    permission_classes = [IsClient]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(cart__user=self.request.user).order_by('-id')
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        wishlist, created = Wishlist.objects.get_or_create(user_id=self.request.user.id)
        comparison, created2 = Comparison.objects.get_or_create(user_id=self.request.user.id)

        queryset = queryset.annotate(
            isLiked=Exists(wishlist.products.all().filter(id__in=OuterRef('product_id')))).annotate(
            isCompared=Exists(comparison.products.all().filter(id__in=OuterRef('product_id'))))

        total = queryset.aggregate(totalSum=Sum(F('orderPrice')))
        if not self.request.query_params.get('p'):
            serializer = self.get_serializer(queryset, many=True)

            return Response({"products": serializer.data, **total})

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return Response({
            "products": self.get_paginated_response(serializer.data).data, **total})


class CartProductDestroyAPIView(DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductCreateSerializer
    permission_classes = [IsClient]
    lookup_field = 'guid'
