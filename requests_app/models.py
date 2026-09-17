from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import BLOOD_GROUP_CHOICES

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('fulfilled', 'Fulfilled'),
    ('cancelled', 'Cancelled'),
]


class BloodRequest(models.Model):
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blood_requests'
    )
    patient_name = models.CharField(max_length=150)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    hospital_name = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    required_date = models.DateField()
    bags_required = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    contact_number = models.CharField(max_length=20)
    description = models.TextField(blank=True, help_text='Reason / additional details.')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.patient_name} needs {self.blood_group} at {self.hospital_name}'
