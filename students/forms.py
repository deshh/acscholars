from django import forms
from .models import Student
from patrons.models import Patron
from subjects.models import Subject

class DateInput(forms.DateInput):
    input_type = 'date'

class StudentForm(forms.ModelForm):


    # multi select check boxes without dropdown
    # patrons = forms.ModelMultipleChoiceField(
    #     queryset=Patron.objects.all(), 
    #     required=False, 
    #     widget=forms.SelectMultiple,
    #     # widget=forms.CheckboxSelectMultiple, 
    #     help_text="Select the patron associated with the student"
    #     )
    patrons = forms.ModelMultipleChoiceField(
        queryset=Patron.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'}),
        help_text="Select the patron associated with the student"
    )

    FUND_ASSISTANCE_CHOICES = ((1, 'Scholership Receiver'), (2, 'Financial Aid Receiver'))


    fund_assistance_type = forms.ChoiceField(
                            widget=forms.RadioSelect,
                            choices=FUND_ASSISTANCE_CHOICES,
                            required=False
                            )


    #single selection from dropdown
    # patrons = forms.ModelChoiceField(
    #     queryset=Patron.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=False,
    #     help_text="Select the patron associated with the student"
    # )


    class Meta:
        model = Student
        fields = ['index_number', 'first_name', 'middle_name', 'last_name', 'is_scholarship_recipient', 'is_financial_aid_recipient', 'fund_assistance_type', 'date_of_birth', 'patrons', 'current_academic_level']

        widgets = {
            'index_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
            'current_academic_level': forms.NumberInput(attrs={'step': "1"}), 
            } 

    def save(self, commit=True):
        student = super().save(commit=False)
        fund_assistance_type = self.cleaned_data['fund_assistance_type']

        # Set field_x and field_y based on the value of yes_or_no
        if fund_assistance_type == '1':
            student.is_scholarship_recipient = True
            student.is_financial_aid_recipient = False
        elif fund_assistance_type == '2':
            student.is_scholarship_recipient = False
            student.is_financial_aid_recipient = True

        if commit:
            student.save()
            self.save_m2m()

        return student
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Check if we have an instance of the Student model (in update mode)
        if self.instance and self.instance.pk:
            if self.instance.is_scholarship_recipient:
                self.initial['fund_assistance_type'] = '1'
            elif self.instance.is_financial_aid_recipient:
                self.initial['fund_assistance_type'] = '2'

class SubjectSelectionForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
