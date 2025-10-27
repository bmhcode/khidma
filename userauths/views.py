from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from userauths.models import User
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, logout, authenticate

# ================= Base view ==================================
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class UserLoginView(LoginView):
    template_name ='userauths/login.html'
    fields = '__all__'
    redirect_authenticated_user = True  
    def get_success_url(self):
        return reverse_lazy('app:posts')

class UserLogoutView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect('app:posts')
         
# =============  End Base view ==========================

# User = settings.AUTH_USER_MODEL
class RegisterPageView(FormView):
    template_name = "userauths/register.html"
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("app:posts")

def registerPage(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username") # form.cleaned_data["username"],
            messages.success(request, f"Hey {username}, Your account was created successfulLy")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("app:posts")
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, "userauths/register.html", context)

# def login(request):
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
                return redirect('app:posts')
            else:
                messages.warning(request, "User Does not Exist, Create an account.")
            
        except:
            messages.warning(request, f"User with {username} does not exist")
        
    return render(request, 'userauths/login.html')

def logoutView(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect('app:posts') #'userauths:login')

