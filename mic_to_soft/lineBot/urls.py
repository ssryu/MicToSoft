from django.urls import path

from . import views

urlpatterns = [
    path('linebot/bank', views.linebot_bank, name='linebot_bank'),
    path('linebot/hotel', views.linebot_hotel, name='linebot_hotel'),
    path('linebot/restaurant', views.linebot_restaurant, name='linebot_restaurant'),
]
