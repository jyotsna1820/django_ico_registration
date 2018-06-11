from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fields = (
        'email', 'eth_address', 'eth_amount', 'country',
        'status', 'editable', 'is_active',
    )

admin.site.register(User, UserAdmin)
