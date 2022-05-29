from django.conf.urls.static import static
from django.urls import path

from task_manager import settings
from . import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', views.HomeView.as_view(), name='home'),
    path('task', views.TaskView.as_view(), name='task'),
    path('task_table', views.TaskTableView.as_view(), name='task_table'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
