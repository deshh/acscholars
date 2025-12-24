from django.db import models
from patrons.models import Patron

    
class Student(models.Model):
    index_number = models.CharField(max_length=50, default='0000')
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, default=None)
    last_name = models.CharField(max_length=255, blank=True, default=None)
    date_of_birth = models.DateField()
    is_scholarship_recipient = models.BooleanField(default=False)
    is_financial_aid_recipient = models.BooleanField(default=False)
    patrons = models.ManyToManyField(Patron, related_name='students')
    current_academic_level = models.IntegerField()

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.index_number} {self.first_name} {self.last_name} "