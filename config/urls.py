"""
URL configuration for config project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('users/', include('users.urls', namespace='users')),
    path('habits/', include('habits.urls', namespace='habits')),
]
