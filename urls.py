from django.urls import path
from . import views

app_name  ='Musify'
urlpatterns = [
    # ex: /polls/
    #path('', views.index, name='index'),
    path('index.html/searchpage.html/', views.search_page, name='searchpage'),
    path('artistpage.html', views.search_page, name='artistpage'),
    path('index.html/displaypage.html/', views.display_page, name='displaypage'),
    path('index.html/', views.redirect_page, name='redirect'),
]
