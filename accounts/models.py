from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


BLOOD_GROUP_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]


class Profile(models.Model):
    """Basic profile information collected at registration for every user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    full_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(
        max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True
    )
    location = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True
    )

    def __str__(self):
        return self.full_name or self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile whenever a new User is created."""
    if created:
        Profile.objects.create(user=instance, full_name=instance.get_full_name() or instance.username)
    else:
        # Make sure a profile always exists (in case of legacy/admin-created users)
        Profile.objects.get_or_create(user=instance)
