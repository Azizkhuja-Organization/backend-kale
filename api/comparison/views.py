from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.comparison.serializers import ComparisonProductDetailSerializer
from api.products.subcategory.serializers import SubCategoryCategoryListSerializer
from common.order.models import Comparison
from common.product.models import SubCategory, Product


class ComparisonAddSubAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        product = Product.objects.filter(id=id).first()
        if product is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        wishlist, created = Comparison.objects.get_or_create(user=request.user)
        if product in wishlist.products.all():
            wishlist.products.remove(product)
        else:
            wishlist.products.add(product)
        return Response(status=status.HTTP_200_OK)


class ComparisonProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comparison, created = Comparison.objects.get_or_create(user_id=2)
        data = []
        products = comparison.products.select_related('category')

        subcategories = SubCategory.objects.all()
        subcategory_products_map = {subcategory.id: [] for subcategory in subcategories}

        for product in products:
            subcategory_products_map[product.category_id].append(product)

        for subcategory in subcategories:
            subcategory_products = subcategory_products_map[subcategory.id]
            if subcategory_products:
                data.append({
                    "category": SubCategoryCategoryListSerializer(subcategory).data,
                    "products": ComparisonProductDetailSerializer(subcategory_products, many=True).data
                })

        return Response(data, status=status.HTTP_200_OK)
