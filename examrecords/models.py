from django.db import models
from students.models import Student
from subjects.models import Subject
from exams.models import Exam

# Create your models here.

class ExamRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()
    grade_awarded = models.CharField(max_length=2, null=False, blank=True, default='')
    special_remarks = models.CharField(max_length=200, null=False, blank=True, default='')

    class Meta:
        unique_together = ['student', 'exam', 'subject']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.exam} - {self.marks_obtained}"

# class ExamRecord(models.Model):
    
#     marks = models.DecimalField(max_digits = 4, 
#                                 decimal_places = 2) 
#     grade_received = models.CharField(max_length=40,null=True)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     # year = models. DateTimeField (null=True)
#     date_reference = models.DateTimeField(default=datetime.now, blank=True)
#     special_remarks = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return f"{self.student} {self.marks}"


#     class Meta:
#         ordering = ["marks"]