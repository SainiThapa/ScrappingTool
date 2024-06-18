from django.urls import path

from . import views

urlpatterns=[
    path('customize',views.customize,name="customize"),
    path('searchresults',views.search,name="search"),
    path('delete/<page_id>',views.delete,name="delete"),
    path('webpage_list',views.webpage_list,name="webpage_list"),
    path('add_webpage',views.add_webpage,name="add_webpage"),
    path('search_database',views.search_database, name="search_database"),
    path('news_datahouse',views.datahouse,name="datahouse"),
    path('feature/<id>',views.feature,name="feature"),
]