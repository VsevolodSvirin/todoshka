from rest_framework.serializers import ModelSerializer

from todolists.models import TodoList


class TodoListSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        fields = ('id', 'name', 'author', 'category', 'date_created', 'date_modified')
        read_only_fields = ('id', 'date_created', 'date_modified')
