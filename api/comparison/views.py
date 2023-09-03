from django.db.models import Exists, OuterRef
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.comparison.serializers import ComparisonProductDetailSerializer
from api.products.subcategory.serializers import SubCategoryCategoryListSerializer
from common.order.models import Comparison, Wishlist, CartProduct
from common.product.models import SubCategory, Product


class ComparisonAddSubAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        product = Product.objects.filter(id=id).first()
        if not product.subcategory:
            return Response(status=status.HTTP_200_OK)

        if product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comparison, created = Comparison.objects.get_or_create(user=request.user)
        if product in comparison.products.all():
            comparison.products.remove(product)
        else:
            comparison.products.add(product)
        return Response(status=status.HTTP_200_OK)


class ComparisonProductsAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        comparison, created = Comparison.objects.get_or_create(user=request.user)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        products = comparison.products.select_related('subcategory').annotate(
            isLiked=Exists(wishlist.products.all().filter(id__in=OuterRef('pk')))).annotate(
            isCart=Exists(CartProduct.objects.filter(product_id=OuterRef('pk'), cart__user_id=self.request.user.id)))
        subcategory = self.request.query_params.get('subcategory')
        if subcategory:
            products = products.filter(subcategory=subcategory)
        subcategories = SubCategory.objects.filter(subcategoryProducts__in=products).distinct()

        return Response({
            "subcategories": SubCategoryCategoryListSerializer(subcategories, many=True).data,
            "products": ComparisonProductDetailSerializer(products, many=True).data
        }, status=status.HTTP_200_OK)
