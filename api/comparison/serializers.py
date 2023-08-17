from rest_framework import serializers

from common.product.models import Product
from config.settings.base import env


class ComparisonProductDetailSerializer(serializers.ModelSerializer):
    photo_small = serializers.SerializerMethodField()
    isLiked = serializers.BooleanField(default=False)

    def get_photo_small(self, product):
        if product.photo_small and not "http" in product.photo_small:
            return env('BASE_URL') + product.photo_small.url
        return None

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'price', 'material', 'size', 'brand', 'manufacturer', 'photo_small',
                  'cornerStatus', 'description', 'isLiked']
