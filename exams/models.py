from django.db import models

# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name