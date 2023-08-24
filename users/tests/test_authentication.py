
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User





class TestCustomUser(TestCase):
    
    def setUp(self):
        self.user={
            'username':'vincent286',
            'email':'vincent@gmail.com',
            'password':'qazwsx123', 
            'password2':'qazwsx123',
            'name':'vinx',
            }
        self.user_short_password={
            'username':'vincent286',
            'email':'vincent@gmail.com',
            'password':'123', 
            'password2':'123',
            'name':'vinx',
            }
        self.user_different_passwords={
            'username':'vincent286',
            'email':'vincent@gmail.com',
            'password':'qazwsx123', 
            'password2':'123qazwsx123',
            'name':'vinx',
            }
        
       
        self.register_url=reverse('users:register')
        self.login_url=reverse('users:login')
        return super().setUp()
    

class RegisterTest(TestCustomUser):  
    def test_user_gets_valid_response(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'registration/register.html')

    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302) 

    def test_cant_register_user_with_shortpassword (self):
        response=self.client.post(self.register_url,self.user_short_password,format='text/html')
        self.assertEqual(response.status_code,400)


    def test_cant_register_user_with_password_not_similar_to_password2 (self):
        response=self.client.post(self.register_url,self.user_different_passwords,format='text/html')
        self.assertEqual(response.status_code,400) 

    def test_cant_register_user_with_already_existing_email (self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,400)  

class LoginTest(TestCustomUser):  
    def test_user_gets_valid_response(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'registration/login.html')

    
    def test_login_success(self):
        self.client.post(self.register_url,self.user,format='text/html')
        user=User.objects.filter(email=self.user['email']).first()
        user.is_active=True
        user.save()
        response=self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cant_login_with_unverified_account(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.client.post(self.login_url,self.user,format='text/html')
        self.assertEqual(response.status_code,401)

    def test_cant_login_with_no_username(self):
        response=self.client.post(self.login_url,{'username':'','password':'qazwsx123'},format='text/html')
        self.assertEqual(response.status_code,401)

    def test_cant_login_with_no_password(self):
        response=self.client.post(self.login_url,{'username':'username','password':''},format='text/html')
        self.assertEqual(response.status_code,401)

