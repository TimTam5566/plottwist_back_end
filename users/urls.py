
from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.CustomUserList.as_view()),
    path('<int:pk>/', views.CustomUserDetail.as_view()),
]


