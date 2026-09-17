import re
from datetime import date

from django import forms

from bloodsync.form_utils import BootstrapFormMixin

from .models import BloodRequest


class BloodRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = [
            'patient_name', 'blood_group', 'hospital_name', 'location',
            'required_date', 'bags_required', 'contact_number', 'description',
        ]
        widgets = {
            'required_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()

    def clean_contact_number(self):
        phone = self.cleaned_data['contact_number']
        if not re.match(r'^\+?\d{7,15}$', phone):
            raise forms.ValidationError('Enter a valid phone number (7-15 digits, optional +).')
        return phone

    def clean_required_date(self):
        required_date = self.cleaned_data['required_date']
        if required_date < date.today():
            raise forms.ValidationError('Required date cannot be in the past.')
        return required_date

    def clean_bags_required(self):
        bags = self.cleaned_data['bags_required']
        if bags <= 0:
            raise forms.ValidationError('Number of bags must be a positive number.')
        return bags


class BloodRequestStatusForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()


class BloodRequestSearchForm(BootstrapFormMixin, forms.Form):
    blood_group = forms.ChoiceField(
        choices=[('', 'Any Blood Group')] + BloodRequest._meta.get_field('blood_group').choices,
        required=False,
    )
    location = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Feni'}),
    )
    status = forms.ChoiceField(
        choices=[('', 'Any Status')] + BloodRequest._meta.get_field('status').choices,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap_classes()
