from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomePageView, LoginView, DashboardView, ProcessingView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("user/", DashboardView.as_view(), name="dashboard"),
    path("processing/", ProcessingView.as_view(), name="processing"),
]
