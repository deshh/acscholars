from django.db import models

# Create your models here.
class Patron(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)


    def __str__(self):
        return self.first_name