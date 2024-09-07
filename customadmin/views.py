from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
def admin_login(request):

    if 'username' in request.session:
        return redirect(admin_home)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        superstatus=user.is_superuser
        print(user,superstatus)
        
        if user is not None and superstatus is True:
            request.session['username']= email
            
            return redirect(admin_home)  # Redirect to the home page on successful login
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'adminlogin.html')
    return render(request,'adminlogin.html')

@never_cache
def admin_home(request):
    if 'username' in request.session:

        users = User.objects.values('username', 'is_staff', 'email', 'date_joined')
        return render(request,'adminhome.html',{'users':users})
    else:
        return render(request,'adminlogin.html')