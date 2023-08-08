from rest_framework import status
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.wishlist.serializers import WishlistDetailSerializer
from common.order.models import Wishlist
from common.product.models import Product


class WishlistAddSubAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        product = Product.objects.filter(id=id).first()
        if product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)
        return Response(status=status.HTTP_200_OK)


class WishlistProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        return Response(WishlistDetailSerializer(wishlist).data, status=status.HTTP_200_OK)
