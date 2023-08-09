from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from api.products.category.serializers import CategoryCreateSerializer
from api.products.images.serializers import ProductImageDetailSerializer
from api.products.subcategory.serializers import SubCategoryListSerializer
from common.product.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'title_uz', 'title_ru', 'title_en', 'description',
                  'description_uz', 'description_ru', 'description_en', 'price', 'material', 'material_uz',
                  'material_ru', 'material_en', 'unit', 'file3D', 'status', 'brand', 'size', 'manufacturer',
                  'manufacturer_uz', 'manufacturer_ru', 'manufacturer_en', 'photo']


class ProductListSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    photo_small = serializers.ImageField(read_only=True)
    isLiked = serializers.BooleanField(default=False)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'title', 'code', 'price', 'brand', 'size', 'manufacturer', 'photo_small',
                  'file3D', 'cornerStatus', 'isLiked']


class ProductDetailSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    photo_medium = serializers.ImageField(read_only=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, product):
        product_images = product.productImages.all()
        return ProductImageDetailSerializer(product_images, many=True).data

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'title_uz', 'title_ru', 'title_en', 'description',
                  'description_uz', 'description_ru', 'description_en', 'price', 'material', 'material_uz',
                  'material_ru', 'material_en', 'unit', 'file3D', 'status', 'brand', 'size', 'manufacturer',
                  'manufacturer_uz', 'manufacturer_ru', 'manufacturer_en', 'photo_medium', 'photos']
