from rest_framework import serializers

from common.product.models import Product
from config.settings.base import env


class WishlistProductDetailSerializer(serializers.ModelSerializer):
    photo_small = serializers.SerializerMethodField()
    isCompared = serializers.BooleanField(default=False)
    isLiked = serializers.BooleanField(default=True)
    isCart = serializers.BooleanField(default=False)

    def get_photo_small(self, product):
        if product.photo_small and not "http" in product.photo_small:
            return env('BASE_URL') + product.photo_small.url
        return None

    class Meta:
        model = Product
        fields = ['id', 'guid', 'code', 'title', 'price', 'material', 'size', 'photo_small', 'cornerStatus',
                  'isCompared', 'isLiked', 'isCart']
