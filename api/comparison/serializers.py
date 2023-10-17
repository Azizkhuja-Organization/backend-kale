from rest_framework import serializers

from common.product.models import Product
from config.settings.base import env


class ComparisonProductDetailSerializer(serializers.ModelSerializer):
    photo_small = serializers.SerializerMethodField()
    isLiked = serializers.BooleanField(default=False)
    isCart = serializers.BooleanField(default=False)
    cartProductQuantity = serializers.IntegerField(default=0)

    def get_photo_small(self, product):
        if product.photo and not "http" in product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'price', 'discountPrice', 'material', 'size', 'brand', 'manufacturer',
                  'photo_small', 'cornerStatus', 'description', 'isLiked', 'isCart', 'cartProductQuantity']
