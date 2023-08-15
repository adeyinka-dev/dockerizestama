from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView,
    AuthPageView,
    DashboardView,
    ProcessingView,
    SignUp,
    Login,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("auth/", SignUp.as_view(), name="auth"),
    path("login/", Login.as_view(), name="login"),
    path("register/", SignUp.as_view(), name="register"),
    path("user/", DashboardView.as_view(), name="dashboard"),
]
