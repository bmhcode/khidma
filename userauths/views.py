from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from userauths.models import User

# User = settings.AUTH_USER_MODEL

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username") # form.cleaned_data["username"],
            messages.success(request, f"Hey {username}, Your account was created successfulLy")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("app:index")
    else:
        form = UserRegisterForm()
        context = {'form':form}
    return render(request, "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already logged In.")
        return redirect("app:index")
    
    elif request.method == 'POST':
        username = request.POST.get("username") # request.POST['username']
        password = request.POST.get("password") # request.POST['password']
        
        try:
            user = User.objects.get(username=username)
            user = authenticate(request,username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect('app:index')
            else:
                messages.warning(request, "User Does not Exist, Create an account.")
            
        except:
            messages.warning(request, f"User with {username} does not exist")
        
    return render(request, 'userauths/sign-in.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect('userauths:sign-in')

