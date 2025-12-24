from django import forms
from .models import ExamRecord
from students.models import Student
from exams.models import Exam
from subjects.models import Subject

class MarkForm(forms.ModelForm):
    
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
        required=True,
        help_text="Select the student"
    )

    exam = forms.ModelChoiceField(
        queryset=Exam.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
        required=True,
        help_text="Select the exam"
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
        required=True,
        help_text="Select the subject"
    )
    
    class Meta:
        model = ExamRecord
        fields = ['student', 'exam', 'subject', 'marks_obtained', 'grade_awarded','special_remarks']

        widgets = {
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.50}),
            'grade_awarded': forms.TextInput(attrs={'class': 'form-control'}),
            'special_remarks': forms.TextInput(attrs={'class': 'form-control'}),
            } 
    