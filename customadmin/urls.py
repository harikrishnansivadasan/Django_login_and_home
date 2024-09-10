from django.urls import path,include
from .import views

urlpatterns = [
    path('login/',views.admin_login,name='adminlogin'),
    path('home/',views.admin_home, name='adminhome'),
    path('add/',views.add,name='add'),
    path('addrec',views.addrec,name='addrec'),
    path('edit/<int:id>/',views.edit,name='edit'),
    path('edit/edituser/<int:user_id>/',views.edituser,name='edituser'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('adminlogout',views.admin_logout,name='adminlogout'),



]
