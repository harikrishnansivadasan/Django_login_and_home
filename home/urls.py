from django.urls import path,include
from .import views

urlpatterns = [
    
    path('home/', views.home,name='home'),
    path('',views.Login,name='login'),
    path('signup',views.Signup,name='signup')

    ]
