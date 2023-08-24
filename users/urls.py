from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
  path('register/', views.RegistrationView.as_view(), name='register'),
  path('login/', views.LoginView.as_view(), name='login'),
  path('logout/', views.LogoutView.as_view(), name='logout'),
  path('activate/<uidb64>/<token>', views.AccountActivateView.as_view(), name='activate')
]