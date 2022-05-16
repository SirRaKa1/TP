from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import TaskTable, Task
from tasks.serializers import TaskSerializer, TaskTableSerializer


class HomeView(LoginRequiredMixin, TemplateView):
    model = TaskTable
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_tables = TaskTable.objects.filter(author=self.request.user)
        task_tables = task_tables.all() if task_tables.exists() else []
        context['task_tables'] = task_tables
        return context


class TaskTableView(LoginRequiredMixin, APIView):

    def get(self, request):
        pk = request.GET.get('task_table_id', None)
        if pk:
            task_table = get_object_or_404(TaskTable, pk=pk)
            if request.user != task_table.author:
                return Response({'status': status.HTTP_400_BAD_REQUEST})
            serializer = TaskSerializer(task_table.tasks.all(), many=True)
            return Response({'status': status.HTTP_200_OK, 'tasks': serializer.data})
        else:
            serializer = TaskTableSerializer(TaskTable.objects.filter(author=request.user), many=True)
            return Response({'status': status.HTTP_200_OK, 'task_tables': serializer.data})

    def post(self, request):
        data = request.data.dict()
        serializer = TaskTableSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({'status': status.HTTP_200_OK, 'task_table': serializer.data})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST})

    def delete(self, request):
        pk = request.POST.get('task_table_id', None)
        task_table = TaskTable.objects.get(pk=pk)
        if request.user != task_table.author:
            return Response({'status': status.HTTP_400_BAD_REQUEST})
        task_table.delete()
        return Response({'status': status.HTTP_200_OK})


class TaskView(LoginRequiredMixin, APIView):

    def post(self, request):
        pk = request.POST.get('task_table_id', None)
        task_table = get_object_or_404(TaskTable, pk=pk)
        if request.user != task_table.author:
            return Response({'status': status.HTTP_400_BAD_REQUEST})
        data = request.data.dict()
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save(task_table=task_table)
            return Response({'status': status.HTTP_200_OK, 'task': serializer.data})
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST})

    def delete(self, request):
        pk = request.POST.get('task_id', None)
        task = Task.objects.get(pk=pk)
        task_table = task.task_table
        if request.user != task_table.author:
            return Response({'status': status.HTTP_400_BAD_REQUEST})
        task.delete()
        return Response({'status': status.HTTP_200_OK, 'task_table_id': task_table.pk})
