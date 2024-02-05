# tasks/urls.py

from django.urls import path
from .views import task_list, home, create_task,user_tasks,update_task

urlpatterns = [
    path('', home, name='home'),
    path('tasks/', task_list, name='task-list'),
    path('tasks/create/', create_task, name='create-task'),
    path('tasks/user/', user_tasks, name='user-tasks'),
    path('tasks/update/<int:task_id>/', update_task, name='update-task'),
    # Add other URL patterns for CRUD operations...
]
