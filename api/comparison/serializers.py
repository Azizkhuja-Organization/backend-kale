from rest_framework import serializers

from common.product.models import Product


class ComparisonProductDetailSerializer(serializers.ModelSerializer):
    photo_small = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'code', 'title', 'price', 'material', 'size', 'brand', 'manufacturer', 'photo_small',
                  'cornerStatus', 'description']
