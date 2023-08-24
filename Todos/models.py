from datetime import datetime,date
from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    todoDetail = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry_date = models.DateField("Expiry Date(mm/dd/yyyy)",auto_now_add=False, auto_now=False, blank=True, null=True)


    def __str__(self):
        return self.todoDetail
