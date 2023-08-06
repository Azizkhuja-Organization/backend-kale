from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from api.products.category.serializers import CategoryCreateSerializer
from api.products.images.serializers import ProductImageDetailSerializer
from common.product.models import Product


class ProductCreateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'category', 'code', 'title', 'title_uz', 'title_ru', 'description', 'description_uz',
                  'description_ru', 'price', 'material', 'material_uz', 'material_ru', 'unit', 'file3D', 'status',
                  'brand', 'size', 'manufacturer', 'manufacturer_uz', 'manufacturer_ru', 'photo']


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    photo_small = serializers.ImageField(read_only=True)
    isLiked = serializers.BooleanField(default=False)

    def get_category(self, product):
        return product.category.title if product.category else None

    class Meta:
        model = Product
        fields = ['id', 'guid', 'category', 'title', 'code', 'price', 'brand', 'size', 'manufacturer', 'photo_small',
                  'file3D', 'cornerStatus', 'isLiked']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryCreateSerializer()
    photo_medium = serializers.ImageField(read_only=True)
    photos = serializers.SerializerMethodField()

    def get_photos(self, product):
        product_images = product.productImages.all()
        return ProductImageDetailSerializer(product_images, many=True).data
        # return [image.imageUrl for image in product_images]

    class Meta:
        model = Product
        fields = ['id', 'guid', 'category', 'code', 'title', 'description', 'price', 'material', 'unit', 'file3D',
                  'status', 'brand', 'size', 'manufacturer', 'photo_medium', 'photos']
