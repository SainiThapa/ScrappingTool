import os

import pandas as pd
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render

from scrappingtool.models import FeaturedNews, Newsheadline, Webportal

from .forms import WebportalForm
from .scrapping import scrape_news, search_and_display, search_news
from .validate import website_data

# Create your views here.

def customize(request):
    user=request.user
    if(user.is_authenticated):
        webportals=Webportal.objects.all()
        return render(request,"customize.html",{'webportals':webportals})
    return render(request,"404.html")

def user_required(user):
    return user.is_active

@user_passes_test(user_required)
def search(request):
    if request.method=="POST":
        # websites=website_data(request)
        search_query = request.POST.get("search")
        matching_newsheadlines = search_and_display(search_query)
        return render(request, "search_result.html", 
                      {'newsheadlines':matching_newsheadlines,
                            'search_query': search_query})
    return redirect("customize")



@user_passes_test(user_required)
def search_database(request):
    if request.method=="POST":
        search_query=request.POST.get("search_query")
        newsheadlines=Newsheadline.objects.all()
        matching_newsheadlines=search_news(newsheadlines,search_query)

        user=request.user
        featuring_news=FeaturedNews.objects.filter(user=user)
        featured_news_objs=[entry.featured_news for entry in featuring_news]
        featured_news_headlines=[object.news_title for object in featured_news_objs]
        
        return render(request, "search_result.html", {'newsheadlines':matching_newsheadlines,'search_query': search_query,
                                                      'featured_news': featured_news_headlines})
    return redirect("customize")



def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def webpage_list(request):
    webportals=Webportal.objects.all()
    return render(request,"webpage_list.html", {'webportals':webportals})

def delete(request,page_id):
    id=page_id.replace("-","")
    print(id)
    webportal=Webportal.objects.filter(page_id=id).first()
    print(webportal)
    webportal.delete()
    return redirect('/tool/webpage_list')

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

@user_passes_test(superuser_required)
def datahouse(request):
    newsheadlines=Newsheadline.objects.all()
    return render(request,"news_list.html",{'newsheadlines':newsheadlines})

@user_passes_test(user_required)
def feature(request,id):
    user=request.user
    if FeaturedNews.objects.filter(user=user,featured_news_id=id).exists():
       raise ValueError("Already exists") 
    else:
        feature_news=FeaturedNews.objects.create(user=user,featured_news_id=id)
    feature_news.save()
    return redirect('/tool/featured_news')

@user_passes_test(user_required)
def unfeature(request,id):
    user=request.user
    feature_news=FeaturedNews.objects.filter(user=user,featured_news_id=id).first()
    feature_news.delete()
    return redirect('/tool/featured_news')

@user_passes_test(user_required)
def featured_news(request):
    featured_news=FeaturedNews.objects.filter(user=request.user)
    return render(request,"featured_news.html",{'featured_news':featured_news})