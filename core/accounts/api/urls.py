from django.urls import path
from .views import RegisterApiView, ProfileApiView
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )


urlpatterns = [
    path("register/", RegisterApiView.as_view(), name="register"),
    path("user/profile/", ProfileApiView.as_view(), name="profile"),
]
