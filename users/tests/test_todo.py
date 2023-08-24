# from django.urls import reverse
# from django.test import TestCase
# from django.contrib.auth.models import User



# class TestCustomUser(TestCase):
    
#     def setUp(self):
#         self.user={
#             'username':'vincent286',
#             'email':'vincent@gmail.com',
#             'password':'qazwsx123', 
#             'password2':'qazwsx123',
#             'name':'vinx',
#             }
        
#         self.register_url=reverse('users:register')
#         self.login_url=reverse('users:login')
#         return super().setUp()
  
# class CreateTodo(TestCustomUser):
#     def test_write_a_new_todo(self):
#       self.client.post(self.register_url,self.user,format='text/html')
#       user=User.objects.filter(email=self.user['email']).first()
#       user.is_active=True
#       user.save()
#       response=self.client.post(self.login_url,self.user,format='text/html')