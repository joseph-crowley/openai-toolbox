from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.submit_message, name='chat'),
    path('select_conversation/', views.select_conversation, name='select_conversation'),
    path('save_conversation/', views.save_conversation, name='save_conversation'),
    path('dalle/', views.dalle, name='dalle'),
]

