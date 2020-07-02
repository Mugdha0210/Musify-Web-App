from django.urls import path
from . import views

app_name  ='Musify'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('searchpage.html/', views.search_page, name='searchpage'),
    path('displaypage.html/', views.display_page, name='displaypage'),
    path('callback.html/', views.redirect_page, name='redirect'),
]
