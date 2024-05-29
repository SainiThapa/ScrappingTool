from django.shortcuts import render
from .models import BaseUser, SuperUser, User

# def CreateUser(request):
#     user=User.objects.create(username="utsav",email="utsav@xyz.com",
#                          password="suman123",is_staff=False, is_superuser=True)
#     user1=SuperUser.objects.create(user=user)
#     user1.save()
#     return render(request,"index.html")