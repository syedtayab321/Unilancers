from django.db import models

# Create your models here.
class SellerSignUpModal(models.Model):
    username = models.CharField(max_length=50)
    university_email = models.EmailField(max_length=100)
    mobile_no = models.CharField(max_length=50)
    university_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    study_field = models.CharField(max_length=50)
    skills = models.CharField(max_length=500)
    Date = models.DateField(auto_now=True)
    password = models.CharField(max_length=12)
    verification_code = models.CharField(max_length=6)