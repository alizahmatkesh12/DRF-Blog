from django.urls import path, include
from .views import RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("api/v1/", include("accounts.api.v1.urls")),
]