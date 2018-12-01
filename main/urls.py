from django.urls import path, include
from . import views

urlpatterns = [
    path('keyboard', views.keyboard, name='keyboard'),
    path('message', views.message, name='message'),
    path('friend', views.friend, name='friend'),
    path('friend/<user_id>', views.friend_delete, name='friend_delete'),
]

