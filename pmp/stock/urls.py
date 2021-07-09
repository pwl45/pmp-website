from django.urls import path

from . import views

urlpatterns = [
    path('', views.home,name="stock-home"),
    #path('about/', views.about,name="stock-about"),
    path('schedule/', views.schedule,name="stock-schedule"),
    path('portfolio/', views.portfolio,name="stock-portfolio"),
    path('portfolio/sort/', views.sortedTable,name="sort-description"),
    path('demo',views.demo,name="demo")
]
