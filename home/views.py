from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page on successful login
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html')

@login_required()
def home(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    return render(request,'home.html')

def Signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')
        
        if password == confirm_password:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()
                messages.success(request, 'User created successfully!')
                return redirect('login')  # Redirect to the login page after successful signup
            else:
                messages.error(request, 'Email is already registered.')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'signup.html')

def logout_page(request):
    logout(request)
    request.session.flush()
    return redirect('login')