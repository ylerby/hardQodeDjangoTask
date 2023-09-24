from django.urls import path
from hardQodeApp import views

urlpatterns = [
    path('', views.get_lessons)
]
