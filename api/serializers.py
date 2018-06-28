from rest_framework.serializers import ModelSerializer

from api.models import TodoList


class TodoListSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        fields = ('name', 'author', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
