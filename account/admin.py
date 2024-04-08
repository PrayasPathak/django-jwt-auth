from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
class UserModelAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "name",
        "tc",
        "is_admin",
    )
    list_filter = ("is_admin",)
    search_fields = (
        "email",
        "name",
    )
    ordering = (
        "email",
        "id",
    )
    filter_horizontal = ()

    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "tc")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2", "tc"),
            },
        ),
    )


admin.site.register(User, UserModelAdmin)
