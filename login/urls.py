from django.contrib import admin
from django.urls import path
from rest_framework. urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
 path('',views.login_user,name ="login"),
 path('accounts/profile/',views.lol,name ="lol"),
 path('create_user/', views.new_user, name='new_user'),
 path('make_newuser/', views.make_newuser, name='make_newuser'),
 



]