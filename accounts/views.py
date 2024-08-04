from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password


from accounts.models import BaseUser, SuperUser
from scrappingtool.models import Webportal, Newsheadline, FeaturedNews

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
        if password==c_password and phone.isdigit():
            # hashed_password = make_password(password)  # Hash the password
            if User.objects.filter(email=email).exists():
                raise ValueError("User with this email already exists")
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'password': make_password(password),
                    'email': email,
                    'is_superuser': False,
                    'is_staff': False,
                }
            )
            if created:
                BaseUser.objects.create(user=user, phone=phone)
            else:
                raise ValueError("User with this username already exists")
            return redirect('login')
        else:
            raise ValueError("Passwords donot match/the Phone number must be in numeric digits")
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
        featurednews=FeaturedNews.objects.all()
        featurednews.delete()
        newsheadlines=Newsheadline.objects.all()
        newsheadlines.delete()
        webportals=Webportal.objects.all()
        webportals.delete()
        auth.logout(request)
    return redirect('/login')