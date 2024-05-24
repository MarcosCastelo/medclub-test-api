from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Additional Info',
            {
                'fields': ('phone_number',),
            }
        )
    )

admin.site.register(User, CustomUserAdmin)