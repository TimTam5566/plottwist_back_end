
'''
The address book for the application - mapping URLs to views.
'''
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    # /users/ → Go to CustomUserList view
    path('', views.CustomUserList.as_view()),
    # /users/1/ → Go to CustomUserDetail view for user with ID 1 (pk1)
    path('<int:pk>/', views.CustomUserDetail.as_view()),
]


