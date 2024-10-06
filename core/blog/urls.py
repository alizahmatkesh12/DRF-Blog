from django.urls import path, include
from . import views
app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="index"),
]
