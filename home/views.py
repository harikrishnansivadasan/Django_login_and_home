from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
def Login(request):
    if 'username' in request.session:
        return redirect(home)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            request.session['username']= email
            
            return redirect('home')  # Redirect to the home page on successful login
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

    
    return render(request, 'login.html')

@never_cache
def home(request):  
    if 'username' in request.session:   
      return render(request,'home.html')
    return redirect(Login)


def Signup(request):
    if 'username' in request.session:   
      return render(request,'home.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if password == confirm_password:
            if not User.objects.filter(email=email).exists():
                try:
                    # Explicitly set username using the email
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.save()
                    messages.success(request, 'User created successfully! Please log in.')
                    return redirect('login')
                except Exception as e:
                    messages.error(request, 'Email is already registered.')
            else:
                messages.error(request, 'Email is already registered.')
        else:
            messages.error(request, 'Passwords do not match.')

        # Re-render the form with email pre-filled and errors displayed
        return render(request, 'signup.html', {'email': email})
    
    return render(request, 'signup.html')

def logout_page(request):
    if 'username' in request.session:
        request.session.flush()
    
    return redirect('login')