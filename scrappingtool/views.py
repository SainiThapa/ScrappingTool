from django.shortcuts import redirect, render

from scrappingtool.models import Webportal
from .validate import website_data
from django.contrib.auth.decorators import user_passes_test
from .forms import WebportalForm
# Create your views here.

def customize(request):
    user=request.user
    if(user.is_authenticated):
        webportals=Webportal.objects.all()
        return render(request,"customize.html",{'webportals':webportals})
    return render(request,"404.html")

def search(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            websites=website_data(request)
            search_query = request.POST.get("search")
            return render(request, "search_result.html", {'websites':websites,'search_query': search_query})
        return redirect("customize")
    return render(request,"404.html")    



def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def webpage_list(request):
    webportals=Webportal.objects.all()
    return render(request,"webpage_list.html", {'webportals':webportals})

@user_passes_test(superuser_required)
def add_webpage(request):
    if request.method=="POST":
        form = WebportalForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('webpage_list')
    else:
        form=WebportalForm()
    return render(request, "add_webportal.html",{'form':form})