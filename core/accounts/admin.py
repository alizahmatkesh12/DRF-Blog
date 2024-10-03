from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class UserAdmin(UserAdmin):
    model = User
    search_fields = ("email",)
    list_display = ("email", "is_superuser", "is_active", "is_verified", "created_date")
    list_filter = ("email", "is_superuser", "is_active", "is_verified")
    ordering = ("-created_date",)
    fieldsets = (
        ("Authentication", {"fields": ("email", "password",)}),
        ("Permissions", {"fields": ("is_staff", "is_verified", "is_active", "is_superuser")}),
        (
            "Group Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    
    
admin.site.register(User, UserAdmin)
admin.site.register(Profile)