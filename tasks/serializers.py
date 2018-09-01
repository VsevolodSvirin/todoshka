from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from tasks.models import Task
from tasks.services import deliver_email_on_update, deliver_email_on_create


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'author', 'assignee', 'category', 'deadline', 'image', 'date_created', 'date_modified')
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
