from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from api.products.subcategory.serializers import SubCategoryListSerializer
from common.product.models import Product
from config.settings.base import env


class ProductCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)
    photos = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'title_uz', 'title_ru', 'title_en', 'description',
                  'description_uz', 'description_ru', 'description_en', 'price', 'material', 'material_uz',
                  'material_ru', 'material_en', 'unit', 'file3D', 'status', 'brand', 'size', 'manufacturer',
                  'manufacturer_uz', 'manufacturer_ru', 'manufacturer_en', 'photo', 'photos']


class ProductUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)
    photos = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'title_uz', 'title_ru', 'title_en', 'description',
                  'description_uz', 'description_ru', 'description_en', 'price', 'material', 'material_uz',
                  'material_ru', 'material_en', 'unit', 'file3D', 'status', 'brand', 'size', 'manufacturer',
                  'manufacturer_uz', 'manufacturer_ru', 'manufacturer_en', 'photo', 'photos']


class ProductListSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    photo_small = serializers.ImageField(read_only=True)
    isLiked = serializers.BooleanField(default=False)
    isCompared = serializers.BooleanField(default=False)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'title', 'code', 'price', 'brand', 'size', 'manufacturer', 'photo_small',
                  'file3D', 'cornerStatus', 'isLiked', 'isCompared', 'status']


class ProductDetailSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    photo_medium = serializers.ImageField(read_only=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, product):
        product_images = product.productImages.all()
        return [{
            "id": productImage.id,
            "guid": productImage.guid,
            "photo_medium": env('BASE_URL') + productImage.photo_medium.url
        } for productImage in product_images if not "http" in productImage.photo_medium.url]

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'title_uz', 'title_ru', 'title_en', 'description',
                  'description_uz', 'description_ru', 'description_en', 'price', 'material', 'material_uz',
                  'material_ru', 'material_en', 'unit', 'file3D', 'status', 'brand', 'size', 'manufacturer',
                  'manufacturer_uz', 'manufacturer_ru', 'manufacturer_en', 'photo_medium', 'photos']
