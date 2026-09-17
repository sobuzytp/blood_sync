from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'blood_group', 'location', 'phone_number')
    list_filter = ('blood_group', 'location')
    search_fields = ('full_name', 'user__username', 'phone_number')
