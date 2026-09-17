import re
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from bloodsync.form_utils import BootstrapFormMixin

from .models import Profile


class RegisterForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(max_length=150, required=True, label='Full Name')
    phone_number = forms.CharField(max_length=20, required=True, label='Phone Number')
    blood_group = forms.ChoiceField(choices=Profile._meta.get_field('blood_group').choices)
    location = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date of Birth',
    )
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'full_name', 'phone_number',
            'blood_group', 'location', 'date_of_birth', 'profile_picture',
            'password1', 'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not re.match(r'^\+?\d{7,15}$', phone):
            raise forms.ValidationError('Enter a valid phone number (7-15 digits, optional +).')
        return phone

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob and dob > date.today():
            raise forms.ValidationError('Date of birth cannot be in the future.')
        return dob

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.profile
            profile.full_name = self.cleaned_data['full_name']
            profile.phone_number = self.cleaned_data['phone_number']
            profile.blood_group = self.cleaned_data['blood_group']
            profile.location = self.cleaned_data['location']
            profile.date_of_birth = self.cleaned_data.get('date_of_birth')
            if self.cleaned_data.get('profile_picture'):
                profile.profile_picture = self.cleaned_data['profile_picture']
            profile.save()
        return user


class ProfileUpdateForm(BootstrapFormMixin, forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = [
            'full_name', 'phone_number', 'blood_group', 'location',
            'date_of_birth', 'profile_picture',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email
        self.apply_bootstrap_classes()

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if phone and not re.match(r'^\+?\d{7,15}$', phone):
            raise forms.ValidationError('Enter a valid phone number (7-15 digits, optional +).')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email__iexact=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if self.user and commit:
            self.user.email = self.cleaned_data['email']
            self.user.save()
        return profile
