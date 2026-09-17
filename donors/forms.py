import re

from django import forms

from bloodsync.form_utils import BootstrapFormMixin

from .models import DonorProfile


class DonorProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = [
            'name', 'blood_group', 'phone_number', 'location',
            'last_donation_date', 'availability', 'description',
        ]
        widgets = {
            'last_donation_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()

    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not re.match(r'^\+?\d{7,15}$', phone):
            raise forms.ValidationError('Enter a valid phone number (7-15 digits, optional +).')
        return phone

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError('Name is required.')
        return name


class DonorSearchForm(BootstrapFormMixin, forms.Form):
    blood_group = forms.ChoiceField(
        choices=[('', 'Any Blood Group')] + DonorProfile._meta.get_field('blood_group').choices,
        required=False,
    )
    location = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Feni'}),
    )
    availability = forms.ChoiceField(
        choices=[('', 'Any Status')] + DonorProfile._meta.get_field('availability').choices,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()
