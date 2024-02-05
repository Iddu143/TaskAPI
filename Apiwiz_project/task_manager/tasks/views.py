# tasks/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

def task_list(request):
    tasks = Task.objects.all()
    data = {'tasks': list(tasks.values())}
    return JsonResponse(data, safe=False)


# Assuming you have a home.html template in the templates folder
def home(request):
    return render(request, 'home.html')


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_task(request):
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the task to the current user
            serializer.save(user=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)


# tasks/views.py

@api_view(['PUT', 'DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'}, status=204)


from .forms import TaskForm

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task-list')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'update_task.html', {'form': form, 'task': task})