from django.urls import path,include
from .import views

urlpatterns = [
    
    path('home/', views.Home),
    path('',views.Login,name='Login'),
    path('signup',views.Signup,name='Signup')
    ]
