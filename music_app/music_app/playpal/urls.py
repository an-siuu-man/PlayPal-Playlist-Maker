from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('songs', views.printSongs, name = 'songs')
]