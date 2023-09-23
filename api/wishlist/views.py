from django.db.models import Exists, OuterRef, F
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.wishlist.serializers import WishlistProductDetailSerializer
from common.order.models import Wishlist, Comparison, CartProduct
from common.product.models import Product


class WishlistAddSubAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        product = Product.objects.filter(id=id).first()
        if product is None:
            return Response({"message": "Product does not found"}, status=status.HTTP_400_BAD_REQUEST)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)
        return Response(status=status.HTTP_200_OK)


class WishlistProductsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        comparison, created2 = Comparison.objects.get_or_create(user_id=self.request.user.id)
        products = wishlist.products.annotate(
            isCompared=Exists(comparison.products.all().filter(id__in=OuterRef('id')))).annotate(
            isCart=Exists(
                CartProduct.objects.filter(product_id=OuterRef('pk'), cart__user_id=self.request.user.id))).order_by(
            '-id').annotate(
            cartProductQuantity=F('cartProduct__quantity'))
        return Response(WishlistProductDetailSerializer(products, many=True).data, status=status.HTTP_200_OK)
