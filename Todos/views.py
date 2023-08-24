from sre_parse import TYPE_FLAGS
import threading
from django.shortcuts import render, redirect
from . models import Todo
from .forms import TodoForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import Http404, HttpResponse, JsonResponse
import datetime
import json

# Create your views here.

class Emailthread(threading.Thread):
    def __init__(self, send_email):
        self.send_email=send_email
        threading.Thread.__init__(self)

    def run(self):
        self.send_email.send()


def index(request):
    """The home page for TodoApp."""
    ExpiredTodoEmail(request)
    return render(request, 'Todos/index.html')

@login_required
def new_todo(request):
    expiredTodos = []
    """the page is to add a new todo"""
    todos = Todo.objects.filter(user=request.user).order_by('date_added')
    if request.method != 'POST':
        form = TodoForm()
    else:
        form = TodoForm(data = request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('Todos:new_todo')
    for todo in todos:
        if datetime.date.today() > todo.expiry_date:
            expiredTodos.append(todo)
    if todos.count() == 0:
        context = {'form': form, 'todos': todos}
        return render(request, 'Todos/new_todo.html', context)
    else:
        context = {'form': form, 'todos': todos, 'expiredTodos':expiredTodos}
        return render(request, 'Todos/new_todo.html', context)
    



@login_required
def edit_todo(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    if todo.user != request.user: 
        raise Http404
    if request.method != 'POST':
        form = TodoForm(instance=todo)
    else:
        form = TodoForm(instance=todo, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('Todos:new_todo')
        
    context = {'todo':todo, 'form':form}
    return render(request, 'Todos/edit_todo.html', context)


def delete_todo(request, todo_id):
    todoDelete = Todo.objects.get(id=todo_id)
    if todoDelete.user != request.user: 
        raise Http404
    todoDelete.delete()
    return redirect('Todos:new_todo')


def completed_todo(request, todo_id):
    todoCompleted = Todo.objects.get(id=todo_id)
    if todoCompleted.user != request.user: 
        raise Http404
    if todoCompleted.status == False:
        todoCompleted.status = True
    else:
        todoCompleted.status = False
    todoCompleted.save()
    return redirect('Todos:new_todo')


def create(request):
    if request.method == 'POST':
        todoDetail = request.POST['todoDetail']
        user = request.user
        expiry_date = request.POST['expiry_date']
        auto_new_todo = Todo(todoDetail=todoDetail,user=user,expiry_date=expiry_date)
        auto_new_todo.save()
        success = 'Todo created successfully.' 
        return HttpResponse(success)

@login_required
def ExpiredTodoEmail(request):
    user = request.user
    try:
        user_details = User.objects.get(username=user)
        email = user_details.email
    except User.DoesNotExist:
        email = None
    Expired_Todos = []
    user=request.user
    todos=Todo.objects.filter(user=user)
    for todo in todos:
        difference=todo.expiry_date - datetime.date.today()
        if difference.days < 2:
            Expired_Todos.append(todo)

    email_subject='Expired Todo tasks in your Account.'
    message=render_to_string('Todos/Expired_Todos.html',
    {
        'user':user,
        'Expired_Todos':Expired_Todos,            
    }
    )
    if len(Expired_Todos)==0:
        print('no expired tasks.')
    else:
        send_email = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        )

        Emailthread(send_email).start()
        print("Email sent")