from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_phone_number', 'default_country')
    search_fields = ('user__username', 'default_country')
