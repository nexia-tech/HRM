from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class User(AbstractUser):
    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200,unique=True)
    employee_id = models.CharField(max_length=200,null=True,blank=True)
    bio = models.TextField(null=True,blank=True)
    shift_duration_hours = models.PositiveIntegerField(default=8)  # Default shift duration in hours
    profile_picture = models.ImageField(null=True,blank=True,upload_to='profile_pics')
    gender = models.CharField(max_length=200,choices=GENDER_CHOICES,default='Male')
    alternative_email = models.EmailField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=200,null=True,blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,null=True,blank=True)
    designation = models.CharField(max_length=200,null=True,blank=True)
    cnic = models.CharField(max_length=200,null=True,blank=True)
    active_password = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.email
    

