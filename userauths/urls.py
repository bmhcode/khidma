from django.urls import path
from userauths import views
from .views import UserLoginView, UserLogoutView
# from django.contrib.auth.views import LogoutView

from django.conf.urls.static import static
from django.conf import settings

app_name = "userauths"

urlpatterns = [
    # path("register/",views.RegisterPageView.as_view(), name="register"),
    path("register/",views.registerPage, name="register"),

    path('login/', UserLoginView.as_view(), name='login'),
    # path("login/",views.login, name="login"),  

    # path('logout/', UserLogoutView.as_view(), name='logout'),
    path("logout/",views.logoutView, name="logout"),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
