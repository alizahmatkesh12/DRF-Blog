from django.urls import path
from ..views import (
    RegisterApiView,
    ChangePasswordAPIView,
    ProfileApiView,
)


urlpatterns = [
    # Registration ---------------------------------------------------
    path("register/", RegisterApiView.as_view(), name="register"),
    # Password ---------------------------------------------------
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    # Profile ---------------------------------------------------    
    path("user/profile/", ProfileApiView.as_view(), name="profile"),
]
