from django.urls import path
from . import views

urlpatterns=[
    path('customize',views.customize,name="customize"),
    path('searchresults',views.search,name="search"),

    path('webpage_list',views.webpage_list,name="webpage_list"),
    path('add_webpage',views.add_webpage,name="add_webpage"),
]