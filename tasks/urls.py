from django.conf.urls.static import static
from django.urls import path

from task_manager import settings
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('task', views.TaskView.as_view(), name='task'),
    path('task_table', views.TaskTableView.as_view(), name='task_table'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
