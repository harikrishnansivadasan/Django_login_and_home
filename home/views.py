import re
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Characters

# Create your views here.
@never_cache
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
    user1=request.session.get('username')
    user=User.objects.get(email=user1)
    context1=user.username 
    print(context1)
    context=Characters.objects.all()
    if 'username' in request.session:   
      return render(request,'home.html',{'context':context, 'context1':context1})
    return redirect(Login)

def password_strength(password):
    if len(password) < 8:
        return False,"Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]',password):
        return False,"Password must contain at least one letter"
    if not re.search(r'[0-9]',password):
        return False,"Password must contain at least one number"
    return True,''

def Signup(request):
    if 'username' in request.session:   
      return render(request,'home.html')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')


        if password == confirm_password:
            is_strong, message = password_strength(password)
            if not is_strong:
                messages.error(request,message)
            else:
                if not User.objects.filter(email=email).exists():
                    try:
                        # Explicitly set username using the email
                        user = User.objects.create_user(username=email, email=email, password=password)
                        user.save()
                        messages.success(request, 'User created successfully! Please log in.')
                        return redirect('login')
                    except Exception as e:
                        messages.error(request, 'Email is already registered.')
                # else:
                #     messages.error(request, 'Email is already registered.')
        else:
            messages.error(request, 'Passwords do not match.')

        # Re-render the form with email pre-filled and errors displayed
        return render(request, 'signup.html', {'email': email})
    
    return render(request, 'signup.html')

@never_cache
def logout_page(request):
    if 'username' in request.session:
        request.session.flush()
    
    return redirect('login')