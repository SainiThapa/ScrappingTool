from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password


from accounts.models import BaseUser, SuperUser

from .decorators import unauthenticated_user

# from accounts.users import CreateUser

# Create your views here.

def home(request):
    # CreateUser(request)
    return render(request,"index.html")


@unauthenticated_user
def signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password1")
        c_password=request.POST.get("password2")
        phone=request.POST.get("phone")
        if password==c_password and phone:
            hashed_password = make_password(password)  # Hash the password
            user=User.objects.create(username=username,password=hashed_password,email=email,is_superuser=False,is_staff=False)
            baseuser=BaseUser.objects.create(user=user,phone=phone)
            baseuser.save()
            return redirect('login')
        else:
            print("Error")
    return render(request,'signup.html')

@unauthenticated_user
def login(request):
    auth.logout(request)
    if request.method=='POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            print("ERROR OCCURED")
    return render(request, "login.html")

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('/login')