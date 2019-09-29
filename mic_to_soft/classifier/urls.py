from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api', views.api, name='api'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('board/', views.board, name='board'),
    path('my_page/', views.my_page, name='my_page'),
]
