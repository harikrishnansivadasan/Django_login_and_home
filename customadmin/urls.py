from django.urls import path,include
from .import views

urlpatterns = [
    path('login/',views.admin_login,name='adminlogin'),
    path('home/',views.admin_home, name='adminhome'),



]
