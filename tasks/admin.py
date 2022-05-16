from django.contrib import admin

from tasks.models import Task, TaskTable

admin.site.register(Task)
admin.site.register(TaskTable)
