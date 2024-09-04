from django.db import models
from UniSeller.models import *
from django.utils import timezone
# Create your models here.
class Buyersignup(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    project_requirements = models.TextField()
    project_budget = models.DecimalField(max_digits=10, decimal_places=2)
    project_deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    userid = models.IntegerField()


class Payment(models.Model):
    client_name = models.CharField(max_length=100)
    provider_name= models.CharField(max_length=100)
    provider_id = models.IntegerField()
    project_paid=models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='GBP')
    stripe_charge_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.amount} {self.currency}"


