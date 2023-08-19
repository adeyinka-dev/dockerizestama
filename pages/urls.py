from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    HomePageView,
    DashboardView,
    ProcessingView,
    SignUp,
    Login,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", Login.as_view(), name="login"),
    path("register/", SignUp.as_view(), name="register"),
    path("user/", DashboardView.as_view(), name="dashboard"),
    path("processing/", ProcessingView.as_view(), name="processing"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
