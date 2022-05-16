from django.contrib.auth.models import User
from django.db import models


class TaskTable(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    date = models.DateTimeField(blank=True)
    task_table = models.ForeignKey(TaskTable, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title
