from rest_framework import serializers

from common.product.models import SubCategory


class SubCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'guid', 'category', 'title']
