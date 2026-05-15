from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'university', 'location', 'joined_at']
    search_fields = ['user__username']
    list_filter   = ['university']
