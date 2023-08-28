from django.urls import path
from django.views.generic import TemplateView
from .views import StamaHome, StamaClient

urlpatterns = [
    path("", StamaHome.as_view(), name="stmhome"),
    path("get-started/", StamaClient.as_view(), name="getstarted"),
    path("thanks/", TemplateView.as_view(template_name="thanks.html"), name="thanks"),
]
