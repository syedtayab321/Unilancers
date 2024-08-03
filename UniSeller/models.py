from django.db import models

# Create your models here.
class SellerSignUpModal(models.Model):
    username = models.CharField(max_length=50)
    university_email = models.EmailField(max_length=100)
    mobile_no = models.CharField(max_length=50)
    university_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    expert_in = models.CharField(max_length=50)
    Date = models.DateField(auto_now=True)
    password = models.CharField(max_length=12)
    status = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=6)