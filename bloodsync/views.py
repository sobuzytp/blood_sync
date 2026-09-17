from django.shortcuts import render

from donors.models import DonorProfile
from requests_app.models import BloodRequest


def home_view(request):
    context = {
        'donor_count': DonorProfile.objects.filter(availability='available').count(),
        'request_count': BloodRequest.objects.filter(status='pending').count(),
        'recent_requests': BloodRequest.objects.filter(status='pending')[:3],
    }
    return render(request, 'home.html', context)


def about_view(request):
    return render(request, 'about.html')
