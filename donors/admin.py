from django.contrib import admin

from .models import DonorProfile


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'location', 'availability', 'last_donation_date')
    list_filter = ('blood_group', 'availability', 'location')
    search_fields = ('name', 'phone_number', 'location')
