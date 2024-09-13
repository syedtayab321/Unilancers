from datetime import date
from django.db import models
from buyer.models import Buyersignup
from django.contrib.auth.models import User

# Create your models here.
class SellerSignUpModal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    profile_picture = models.FileField(upload_to='profile_pictures/')
    university_email = models.EmailField(max_length=100)
    mobile_no = models.CharField(max_length=50)
    university_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    study_field = models.CharField(max_length=50)
    skills = models.CharField(max_length=500)
    Date = models.DateField(auto_now=True)
    password = models.CharField(max_length=12)
    verification_code = models.CharField(max_length=6)

    def __str__(self):
        return self.username

class ProjectAppliedModal(models.Model):
    project_name = models.CharField(max_length=50)
    posted_by = models.CharField(max_length=50,default='noone')
    seller_id = models.IntegerField()
    project_price=models.IntegerField()
    project_tokens=models.IntegerField()
    Date_from=models.DateField()
    Date_to=models.DateField()
    applied_date=models.DateField(default=date.today)
    cover_letter=models.CharField(max_length=5000)
    status=models.CharField(max_length=50,default='pending')

    def __str__(self):
        return self.project_name

class GigDataModal(models.Model):
    seller_id = models.IntegerField()
    gig_title = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    sub_field = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    gig_image1 = models.FileField(upload_to='gig_images/')
    gig_image2 = models.FileField(upload_to='gig_images/')
    gig_image3 = models.FileField(upload_to='gig_images/')

    def __str__(self):
        return self.field

    def delete(self, *args, **kwargs):
        # Delete the files from the file system
        self.gig_image1.delete(save=False)
        self.gig_image2.delete(save=False)
        self.gig_image3.delete(save=False)
        super().delete(*args, **kwargs)

class SellerFeedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name}"