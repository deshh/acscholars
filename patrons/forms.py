from django import forms
from .models import Patron
from django.core.exceptions import ValidationError
import re

class PatronForm(forms.ModelForm):
    class Meta:
        model = Patron
        fields = ['first_name', 'last_name', 'email', 'phone', 'amount']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),          
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Get the instance being updated
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        # If instance exists, exclude the email field from validation
        if self.instance and self.instance.pk:
            self.fields['email'].validators = []

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Patron.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("A patron with this email already exists.")
        return email
        # email = self.cleaned_data.get('email')
        # if Patron.objects.filter(email=email).exists():
        #     raise ValidationError("A patron with this email already exists.")
        # return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValidationError("Enter a valid phone number.")
        return phone

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError("The amount must be greater than zero.")
        return amount