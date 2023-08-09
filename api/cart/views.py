from django.db.models import F, Sum, Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.cart.serializers import CartProductCreateSerializer, CartProductListSerializer
from api.paginator import CustomPagination
from api.permissions import IsClient
from common.order.models import Cart, CartProduct, Wishlist
from common.product.models import Product


# CART

class CountersAPIView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            cartProducts = CartProduct.objects.filter(cart__user=request.user).count()
            wishlistProducts, created = Wishlist.objects.get_or_create(user=request.user)
            response = {
                'inCart': cartProducts,
                'inWishlist': wishlistProducts.products.count()
            }
        else:
            response = {
                'inCart': 0,
                'inWishlist': 0
            }

        return Response(response, status=status.HTTP_200_OK)


class CartAddSubAPIView(APIView):
    permission_classes = [IsClient]

    def get(self, request):
        id = request.query_params.get('id')
        product = Product.objects.filter(id=id).first()
        if not product:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        action = request.query_params.get('action')
        if action is not None and action in ['add', 'sub']:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cartProducts = cart.cartCartProduct.all().select_related('cart', 'product')
            cartProduct = cartProducts.filter(product=product, cart=cart).first()
            if cartProduct is None and action == 'add':
                CartProduct.objects.create(cart=cart, product=product, orderPrice=product.amount)
            elif action == 'add' and cartProduct:
                cartProduct.add
            elif action == 'sub' and cartProduct:
                if cartProduct.quantity == 1:
                    cartProduct.delete()
                cartProduct.sub
        return Response(status=status.HTTP_200_OK)


# CART PRODUCTS

class CartProductCreateAPIView(CreateAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductCreateSerializer
    permission_classes = [IsClient]


class CartProductListAPIView(ListAPIView):
    queryset = CartProduct.objects.select_related('cart', 'cart__user', 'product').all()
    serializer_class = CartProductListSerializer
    # permission_classes = [IsClient]

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(cart__user=self.request.user)
        queryset = queryset.filter(cart__user_id=2)
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        p = self.request.query_params.get('p')
        if p:
            self.pagination_class = CustomPagination
        # queryset.aggregate(totalSum=Sum(F('orderPrice')))
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.aggregate(totalSum=Sum(F('orderPrice')))
        totalDiscount = queryset.aggregate(totalDiscount=Sum(F('product__price')))
        if not self.request.query_params.get('p'):
            serializer = self.get_serializer(queryset, many=True)

            return Response({"products": serializer.data, **total, **totalDiscount})

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        # if page is not None:
        return Response({"products": self.get_paginated_response(serializer.data).data, **total, **totalDiscount})
        # elif page:
            # return Response({"products": self.get_paginated_response(serializer.data).data, **total, **totalDiscount})


class CartProductDestroyAPIView(DestroyAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductCreateSerializer
    permission_classes = [IsClient]
    lookup_field = 'guid'
