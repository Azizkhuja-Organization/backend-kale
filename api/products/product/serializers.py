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
                  'description_uz', 'description_ru', 'description_en', 'price', 'discountPrice', 'material', 'material_uz',
                  'material_ru', 'material_en', 'unit', 'file3D', 'status', 'brand', 'size', 'manufacturer',
                  'manufacturer_uz', 'manufacturer_ru', 'manufacturer_en', 'photo', 'photos', 'cornerStatus', 'isTop',
                  'quantity']


class ProductUpdateSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False)
    photos = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'code', 'title', 'title_uz', 'title_ru', 'title_en', 'description',
                  'description_uz', 'description_ru', 'description_en', 'price', 'discountPrice', 'material', 'material_uz',
                  'material_ru', 'material_en', 'unit', 'file3D', 'status', 'brand', 'size', 'manufacturer',
                  'manufacturer_uz', 'manufacturer_ru', 'manufacturer_en', 'photo', 'photos', 'cornerStatus', 'isTop',
                  'quantity']


class ProductListSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    # photo_small = serializers.ImageField(read_only=True)
    photo_small = serializers.SerializerMethodField()
    isCompared = serializers.BooleanField(default=False)
    discountPrice = serializers.SerializerMethodField()

    def get_photo_small(self, product):
        if product.photo and not "http" in product.photo:
            return env('BASE_URL') + product.photo.url
        return None

    def get_discountPrice(self, product):
        if product.discountPrice == product.price or product.discountPrice > product.price:
            return None
        else:
            return product.discountPrice


    class Meta:
        model = Product
        fields = ['id', 'guid', 'subcategory', 'title', 'code', 'price', 'discountPrice', 'brand', 'size', 'manufacturer',
                  'photo_small', 'file3D', 'cornerStatus', 'isCompared', 'status', 'isTop', 'quantity']


class ProductDetailSerializer(serializers.ModelSerializer):
    subcategory = SubCategoryListSerializer()
    # photo_medium = serializers.ImageField(read_only=True)
    photo_medium = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    isCompared = serializers.BooleanField(default=False)

    def get_photo_medium(self, product):
        if product.photo and not "http" in product.photo:
            return env('BASE_URL') + product.photo.url
        return None

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
                  'description_uz', 'description_ru', 'description_en', 'price', 'discountPrice', 'material', 'material_uz',
                  'material_ru', 'material_en', 'unit', 'file3D', 'status', 'brand', 'size', 'manufacturer',
                  'manufacturer_uz', 'manufacturer_ru', 'manufacturer_en', 'photo_medium', 'photos',
                  'isCompared', 'cornerStatus', 'isTop', 'quantity']


class ProductOneSerializerFor1C(serializers.Serializer):
    Наименование = serializers.CharField(max_length=100)
    Код = serializers.CharField(allow_blank=True, max_length=50)
    ЕдиницаИзмерения = serializers.CharField(max_length=5)
    ТорговаяМарка = serializers.CharField(allow_blank=True)
    Размеры = serializers.CharField(allow_blank=True)
    Описание = serializers.CharField(allow_blank=True)
    Производитель = serializers.CharField(allow_blank=True)
    Категория = serializers.CharField(allow_blank=True)
    Брэнд = serializers.CharField()


class Product1CCreateUpdateSerializer(serializers.Serializer):
    Товары = ProductOneSerializerFor1C(many=True)


class ProductAll1CDestroySerializer(serializers.Serializer):
    Код = serializers.CharField(max_length=50)


class Product1CDestroySerializer(serializers.Serializer):
    Товары = ProductAll1CDestroySerializer(many=True)
