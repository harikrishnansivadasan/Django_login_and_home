from django.urls import path,include
from .import views

urlpatterns = [
    
    path('',views.Login,name='login'),
    path('login',views.Login,name='login'),
    path('home/', views.home,name='home'),
    path('signup',views.Signup,name='signup'),
    path('logout',views.logout_page,name='logout')

    ]
