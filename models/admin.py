"""
Администраторская панель управления задачами
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
# from .models import Task
# from .forms import TaskForm


def is_admin(user):
    """
    Проверяет, является ли пользователь администратором системы
    
    Args:
        user (User): Объект пользователя Django
    """
    return user.is_superuser


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_panel_view(request):
    """
    Отображает главную страницу администраторской панели
    
    Args:
        request (HttpRequest): HTTP-запрос от клиента
    """
    users = User.objects.prefetch_related('tasks').all()
    
    context = {
        'users': users,
        'page_title': 'Админ-панель'
    }
    return render(request, 'admin_panel.html', context)


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_task_create_view(request, user_id):
    """
    Создаёт новую задачу для указанного пользователя от имени администратора
    
    Args:
        request (HttpRequest): HTTP-запрос от клиента
        user_id (int): ID пользователя, которому будет назначена задача
    """
    target_user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = target_user
            task.save()
            return redirect('admin_panel')
    else:
        form = Task Form()
    
    context = {
        'form': form,
        'target_user': target_user,
        'editing': False,
        'page_title': f'Создать задачу для {target_user.username}'
    }
    return render(request, 'task_form.html', context)


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_task_update_view(request, task_id):
    """
    Редактирует существующую задачу любого пользователя
    Args:
        request (HttpRequest): HTTP-запрос от клиента
        task_id (int): ID редактируемой задачи
    """
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
        'target_user': task.user,
        'editing': True,
        'page_title': f'Редактировать задачу: {task.title}'
    }
    return render(request, 'task_form.html', context)


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def admin_task_delete_view(request, task_id):
    """
    Удаляет задачу любого пользователя

    Args:
        request (HttpRequest): HTTP-запрос от клиента
        task_id (int): ID удаляемой задачи
    """
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task.delete()
        return redirect('admin_panel')
    
    context = {
        'task': task,
        'page_title': f'Удалить задачу: {task.title}'
    }
    return render(request, 'task_confirm_delete.html', context)
