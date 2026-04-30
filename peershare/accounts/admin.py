from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'university_email', 'is_verified', 'date_joined']
    list_filter   = ['is_verified']
    search_fields = ['username', 'university_email']
    fieldsets     = UserAdmin.fieldsets + (
        ('University Info', {'fields': ('university_email', 'is_verified')}),
    )