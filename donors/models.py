from django.conf import settings
from django.db import models

from accounts.models import BLOOD_GROUP_CHOICES

AVAILABILITY_CHOICES = [
    ('available', 'Available'),
    ('not_available', 'Not Available'),
]


class DonorProfile(models.Model):
    """A user opts in to become a donor by creating this profile."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donor_profile'
    )
    name = models.CharField(max_length=150)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    last_donation_date = models.DateField(null=True, blank=True)
    availability = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default='available'
    )
    description = models.TextField(blank=True, help_text='A short description about yourself.')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.name} ({self.blood_group})'

    @property
    def is_available(self):
        return self.availability == 'available'
