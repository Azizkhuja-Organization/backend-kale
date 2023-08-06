from rest_framework import serializers

from common.product.models import Category, SubCategory


class SubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'category', 'title', 'title_uz', 'title_ru', 'title_en']


class SubCategoryCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'guid', 'title']


class SubCategoryListSerializer(serializers.ModelSerializer):
    category = SubCategoryCategoryListSerializer()

    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'category', 'title']


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, sub):
        if sub.category:
            return sub.category.title
        return None

    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'category', 'title', 'title_uz', 'title_ru', 'title_en']
