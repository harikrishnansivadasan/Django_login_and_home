from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
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
        user=User.objects.get(email=email)
        name=user.username
        
        user = authenticate(request, username=email, password=password) or authenticate(request,email=email,password=password)
        if user is not None:
            superstatus=user.is_superuser
            staffstatus=user.is_staff
            print(user,superstatus)
        
            if user is not None and (superstatus is True or staffstatus is True):
                request.session['username']= email
                
                return redirect(admin_home)  # Redirect to the home page on successful login
            else:
                messages.error(request, 'No admin provision')
                return render(request, 'adminlogin.html')
    return render(request,'adminlogin.html')

@never_cache
def admin_home(request):
    if 'username' in request.session:
        username=request.session.get('username')
        user = User.objects.get(username=request.session.get('username'))
        superstatus=user.is_superuser
        staffstatus=user.is_staff
        if superstatus or staffstatus:

            query=request.GET.get('q','')
            if query:
                users=User.objects.filter(username__icontains=query ).values('id','username', 'is_staff', 'email','is_superuser', 'date_joined')
            else:
                users = User.objects.values('id','username', 'is_staff', 'email','is_superuser', 'date_joined')

            return render(request, 'adminhome.html', {'users': users, 'superstatus': superstatus, 'name':username})
        else:
            messages.error(request,'only staff and superuser have permission to login')
            return render(request, 'adminlogin.html')
           
    else:
        return render(request, 'adminlogin.html')
    
@never_cache
def add(request):
    if 'username' in request.session:
        return render(request,'add.html')
    else:
        return render(request, 'adminlogin.html')

@never_cache
def addrec(request):
    if 'username' in request.session:
        if request.method == 'POST':
            # Get data from the form
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            is_superuser = 'is_superuser' in request.POST
            is_staff = 'is_staff' in request.POST

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('add')  # Replace with your view where the form is
            else:
                # Create the user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_superuser=is_superuser,
                    is_staff=is_staff
                )
                user.save()
                messages.success(request, 'User added successfully!')
                return redirect('adminhome')  # Replace with your view where the form is

        return render(request, 'add')
    else:
        return render(request, 'adminlogin.html')

@never_cache
def edit(request,id):
    if 'username' in request.session:
        user=User.objects.get(id=id)
        return render(request,'edit.html',{'user':user})
    else:
        return render(request, 'adminlogin.html')

@never_cache
def edituser(request, user_id):
    if 'username' in request.session:
        user = get_object_or_404(User, id=user_id)
        
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            is_superuser = 'is_superuser' in request.POST
            is_staff = 'is_staff' in request.POST
            
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.set_password(password)
            user.is_superuser = is_superuser
            user.is_staff = is_staff
            user.save()
            
            messages.success(request, 'User updated successfully!')
            return redirect('adminhome')  # Redirect to a view of your choice
        
        return render(request, 'edit.html', {'user': user})
    else:
        return render(request, 'adminlogin.html')

@never_cache
def delete(request,id):
    if 'username' in request.session:
        user=User.objects.get(id=id)
        user.delete()
        return redirect('adminhome')
    else:
        return render(request, 'adminlogin.html')


@never_cache
def admin_logout(request):
    
    request.session.flush()
    
    return redirect('adminlogin')

        
    
    