"""
URL configuration for rater project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.views.generic.base import TemplateView

from accounts import views as views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index),
    path('add', views.add),
    path('edit/<int:rating_id>', views.edit),
    path('login/', views.custom_login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('settings', views.settings, name='settings'),
    path('settheme/<int:account_id>/', views.settheme, name='settheme'),

]
