from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'code': forms.TextInput(attrs={'class': 'form-control'}), 
                } 
