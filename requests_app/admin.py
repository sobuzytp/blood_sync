from django.contrib import admin

from .models import BloodRequest


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'hospital_name', 'location', 'required_date', 'status')
    list_filter = ('blood_group', 'status', 'location')
    search_fields = ('patient_name', 'hospital_name', 'location', 'contact_number')
