# defines urls for the Todos app
from django.urls import path
from . import views

app_name = 'Todos'
urlpatterns = [
    path('',views.index, name='index'),
    path('new_todo/', views.new_todo, name='new_todo'),
    path('edit_todo/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('completed_todo/<int:todo_id>/', views.completed_todo, name='completed_todo'),
    path('create', views.create, name='create'),
]