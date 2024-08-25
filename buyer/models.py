from django.db import models
from UniSeller.models import *
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

class ProjectTransactions(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(SellerSignUpModal, on_delete=models.CASCADE)
    client = models.ForeignKey(Buyersignup, on_delete=models.CASCADE, related_name='client_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed')])
    admin_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
