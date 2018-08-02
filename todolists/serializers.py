import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from todolists.models import TodoList


class TodoListSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        fields = ('id', 'name', 'author', 'assignee', 'category', 'deadline', 'date_created', 'date_modified')
        read_only_fields = ('id', 'date_created', 'date_modified')

    def validate(self, attrs):
        if attrs.get('deadline') and datetime.datetime.now() > attrs['deadline']:
            raise serializers.ValidationError("deadline must occur after task is created")
        return attrs
