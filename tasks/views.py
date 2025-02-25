from django.shortcuts import render, redirect, get_object_or_404

# Esto es para crear un usuario
from django.contrib.auth.forms import UserCreationForm

# Esto es para comprobar si el usuario existe
from django.contrib.auth.forms import AuthenticationForm

# Clase para crear usuarios
from django.contrib.auth.models import User
from django.http import HttpResponse

# Modulo de django de auth que crea cookie
from django.contrib.auth import login, logout

# Metodo para autentificar la sesion
from django.contrib.auth import authenticate

# Manejar error de integridad en la base de datos
from django.db import IntegrityError

# Esto es para que algunos nada mas puedan acceder
from django.contrib.auth.decorators import login_required

from .forms import TaskForm
from .models import Task

from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'home.html')


def signup(request):
    """
    Vista encargada de registrar un usuario
    """
    if request.method == 'GET':
        print('\nEnviando formulario...')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        print('')
        print('')
        print('Obteniendo datos...')
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            # Register user
            try:
                print('Registrando usuario...')
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': "Username already exist"
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Pasword do not match'
            })

@login_required
def tasks(request):
    tasks = Task.objects.filter(
        user_owner=request.user,
        date_completed__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user_owner=request.user,
        date_completed__isnull=False
        ).order_by('-date_completed')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def create_task(request):
    '''
    Para el requeste, el usuario es user
    pero para las tareas el usuario se guarda en
    user.owner
    '''

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': request.GET.get('error', '')
        })
    elif request.method == 'POST':
        try:
            task_form = TaskForm(request.POST)
            new_task = task_form.save(commit=False)
            new_task.user_owner = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return redirect('/tasks/create/?error=Please provide valid data')

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user_owner=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': request.GET.get('error', '')
        })
    elif request.method == 'POST':
        try:
            task = get_object_or_404(Task, pk=task_id, user_owner=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return redirect(f'/tasks/{task_id}/?error=Please provide valid data')

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user_owner=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user_owner=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    """
    Vista encargada de cerrar sesion
    """
    logout(request)
    return redirect('home')


def signin(request):
    """
    Vista encargada de iniciar sesion
    """
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error': request.GET.get('error', '')
        })
    elif request.method == 'POST':
        """
        Authenticate me devuelve un usuario si este es valido
        si no es valido este usuario estara vacio
        """
        print(request.POST)
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is None:

            return redirect('/signin/?error=Username or password is incorrect')
            # """
            # Este metodo genera que a la hora de recargar la pagina
            # lo que pase es que se vuelve a enviar el formulario
            # entonces utilizamos el de mas arriba que soluciona este
            # error
            # """
            # return render(request, 'signin.html', {
            #     'form': AuthenticationForm,
            #     'error': 'Username or password is incorrect'
            # })

        else:
            login(request, user)
            return redirect('tasks')
