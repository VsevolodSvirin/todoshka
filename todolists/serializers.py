from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from todolists.models import TodoList
from todolists.services import deliver_email_on_update, deliver_email_on_create


class TodoListSerializer(ModelSerializer):
    class Meta:
        model = TodoList
        fields = ('id', 'name', 'author', 'assignee', 'category', 'deadline', 'date_created', 'date_modified')
        read_only_fields = ('id', 'date_created', 'date_modified')

    def validate(self, attrs):
        if attrs.get('deadline') and timezone.now() > attrs['deadline']:
            raise serializers.ValidationError('deadline must occur after task is created')
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        deliver_email_on_create(instance, validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        deliver_email_on_update(instance, validated_data)
        return instance
