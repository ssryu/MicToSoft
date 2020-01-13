from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api', views.api, name='api'),
    path('board/models/', views.board_models, name='models'),
    path('board/models/<int:pk>', views.model_detail, name='model_detail'),
    path('board/models/create', views.model_create, name='model_create'),
    path('board/models/<int:pk>', views.model_edit, name='model_edit'),
]
