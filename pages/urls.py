from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    HomePageView,
    DashboardView,
    SignUp,
    Login,
    EditInfo,
    RepairHistoryView,
    TestPage,
)

urlpatterns = [
    path("test/", TestPage.as_view(), name="test"),
    path("", HomePageView.as_view(), name="home"),
    path("login/", Login.as_view(), name="login"),
    path("register/", SignUp.as_view(), name="register"),
    path(
        "registration-successful/",
        TemplateView.as_view(template_name="register_success.html"),
        name="register_success",
    ),
    path("user/", DashboardView.as_view(), name="dashboard"),
    path("repair-history/", RepairHistoryView.as_view(), name="repair_history"),
    path("edit-profile/<int:pk>/", EditInfo.as_view(), name="edit_profile"),
    path(
        "update-success/",
        TemplateView.as_view(template_name="edit_success.html"),
        name="update_success",
    ),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
