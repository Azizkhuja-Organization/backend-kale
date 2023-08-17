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


class ComparisonProductsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comparison, created = Comparison.objects.get_or_create(user=request.user)
        data = []
        products = comparison.products.select_related('subcategory')
        if self.request.query_params.get('all'):
            return Response(ComparisonProductDetailSerializer(products, many=True).data, status=status.HTTP_200_OK)
        subcategories = SubCategory.objects.all()
        subcategory_products_map = {subcategory.id: [] for subcategory in subcategories}

        for product in products:
            if product.subcategory:
                subcategory_products_map[product.subcategory_id].append(product)

        for subcategory in subcategories:
            subcategory_products = subcategory_products_map[subcategory.id]
            if subcategory_products:
                data.append({
                    "subcategory": SubCategoryCategoryListSerializer(subcategory).data,
                    "products": ComparisonProductDetailSerializer(subcategory_products, many=True).data
                })

        return Response(data, status=status.HTTP_200_OK)
