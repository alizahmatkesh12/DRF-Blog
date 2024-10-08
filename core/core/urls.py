from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="API for Blog project Models",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="alizahmatkesh12@gmial.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("blog.urls")),
    # accounts app
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # api authentication 
    path('api-auth/', include('rest_framework.urls')),
    #api swagger
    path("swagger/api.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/",schema_view.with_ui("swagger", cache_timeout=0),name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)