from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class UserAdmin(UserAdmin):
    model = User
    search_fields = ("email",)
    list_filter = ("email", "is_active", "is_staff")
    list_display = ("email", "is_active", "is_staff")
    ordering = ("-created_date",)
    fieldsets = (
        ("Authentication", {"fields": ("email",)}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        (
            "Group Permissions",
            {
                "fields": (
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
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
                    "is_staff",
                ),
            },
        ),
    )
    
    
admin.site.register(User, UserAdmin)
admin.site.register(Profile)