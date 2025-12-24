from django import forms
from .models import Exam


class ExamForm(forms.ModelForm):
    
    class Meta:
        model = Exam
        fields = ['name', 'date']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
            } 