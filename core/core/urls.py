from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions


urlpatterns = [
    path('admin/', admin.site.urls),
    # accounts app
    path("accounts/", include("accounts.urls")),
    
    # api authentication 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
