from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView,
    DashboardView,
    SignUp,
    Login,
    EditInfo,
    RepairHistoryView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("login/", Login.as_view(), name="login"),
    path("register/", SignUp.as_view(), name="register"),
    path("user/", DashboardView.as_view(), name="dashboard"),
    path("repair_history/", RepairHistoryView.as_view(), name="repair_history"),
    path("edit/<int:pk>/", EditInfo.as_view(), name="edit"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
