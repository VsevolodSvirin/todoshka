from rest_framework.serializers import ModelSerializer

from categories.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'common')
        read_only_fields = ('id', 'common')
