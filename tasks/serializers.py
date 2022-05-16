from rest_framework import serializers

from tasks.models import Task, TaskTable


class TaskTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTable
        fields = ['id', 'title']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'date']
