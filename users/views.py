
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
import threading


class Emailthread(threading.Thread):
    def __init__(self, email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        context={
            'data':request.POST,
            'has_error':False,
        }
        email=request.POST.get('email')
        username=request.POST.get('username')
        full_name=request.POST.get('name')
        password=request.POST.get('password')
        password2=request.POST.get('password2')

        try:
            if len(password)<6:
                messages.add_message(request, messages.ERROR, 'Passwords should atleast be 6 characters long.')
                context['has_error']=True
        except Exception as identifier:
            pass

        if password != password2:
            messages.add_message(request, messages.ERROR, 'Passwords do not match.')
            context['has_error']=True
        
        # try:
        #     if not validate_email(email):
        #         print('strong')
        #         messages.add_message(request, messages.ERROR, 'Please provide a valid email.')
        #         context['has_error']=True
        # except Exception as identifier:
        #     pass

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken.')
                context['has_error']=True
        except Exception as identifier:
            pass

        try:
            if User.objects.filter(username=username).first():
                messages.add_message(request, messages.ERROR, 'Username is taken.')
                context['has_error']=True
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'registration/register.html', context, status=400)
        
        user=User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.first_name=full_name
        user.last_name=full_name
        user.is_active=False

        user.save()



        current_site=get_current_site(request)
        email_subject='Activate your Account.'
        message=render_to_string('registration/activate.html',
        {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)                   
        }
        )


        email_message = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        )

        

        Emailthread(email_message).start()




        messages.add_message(request, messages.SUCCESS, 'Account is created successfully.')

        return redirect('users:login')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')
    
    def post(self, request):
        context={
            'data':request.POST,
            'has_error':False
        }
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        
        try:
            user_details = User.objects.get(username=username)
            email = user_details.email
            user_email = User.objects.get(email=email)
            if not user_email.is_active:
                messages.add_message(request, messages.ERROR, 'Check your email to verify your account.')
        except Exception as identifier:
            pass

        if username=='':
            messages.add_message(request,messages.ERROR, 'Username is required.')
            context['has_error']=True

        if password=='':
            messages.add_message(request,messages.ERROR, 'Password is required.')
            context['has_error']=True

        user=authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request,messages.ERROR, 'Invalid login.')
            context['has_error']=True

        if context['has_error']:
            return render(request, 'registration/login.html', status=401, context=context)
        
        login(request, user)
        return redirect('Todos:index')
    



class AccountActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None 

        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.add_message(request,messages.INFO, 'Account activated successfully.')
            return redirect('users:login')
        return render(request, 'registration/activation_failed.html', status=401)
    
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.add_message(request,messages.SUCCESS, 'Logged out successfully.')
        return render(request, 'registration/login.html')
    
    