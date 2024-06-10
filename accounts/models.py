from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User=get_user_model()

class SuperUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username

class BaseUser(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.IntegerField()

    def __str__(self) -> str:
        return self.user.username

    