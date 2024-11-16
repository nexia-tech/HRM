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
    employee_id = models.CharField(max_length=200,unique=True,null=True)
    shift_duration_hours = models.PositiveIntegerField(default=8)  # Default shift duration in hours
    profile_picture = models.ImageField(null=True,blank=True,upload_to='profile_pics')
    gender = models.CharField(max_length=200,choices=GENDER_CHOICES,default='Male')
    phone = models.CharField(max_length=200,null=True,blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,null=True,blank=True)
    designation = models.CharField(max_length=200,null=True,blank=True)
    cnic = models.CharField(max_length=200,null=True,blank=True)
    active_password = models.CharField(max_length=200,null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    martial_status = models.CharField(max_length=250,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    working_status = models.CharField(max_length=200,null=True,blank=True)
    
    company_email = models.EmailField(max_length=200,null=True,blank=True)
    company_phone_number = models.CharField(max_length=200,null=True,blank=True)
    emergency_contact_name = models.CharField(max_length=200,null=True,blank=True)
    emergency_contact_number = models.CharField(max_length=200,null=True,blank=True)
    emergency_contact_relationship = models.CharField(max_length=200,null=True,blank=True)
    
    doj = models.DateField(null=True,blank=True)
    shift_timings = models.TimeField(null=True,blank=True)
    shift_end_timing = models.TimeField(null=True,blank=True)
    employment_status = models.CharField(max_length=250,null=True,blank=True)
    supervisor_name = models.CharField(max_length=250,null=True,blank=True)
    job_description = models.TextField(null=True,blank=True)
    
    matric_details = models.JSONField(null=True,blank=True)
    intermediate_details = models.JSONField(null=True,blank=True)
    bachelors_details = models.JSONField(null=True,blank=True)
    masters_details = models.JSONField(null=True,blank=True)
    phd_details = models.JSONField(null=True,blank=True)
    diploma_details = models.JSONField(null=True,blank=True)
    job_experience = models.JSONField(null=True,blank=True)

    basic_salary = models.CharField(max_length=250,null=True,blank=True)
    fuel_allowance = models.CharField(max_length=250,null=True,blank=True)
    other_allowance = models.CharField(max_length=250,null=True,blank=True)
    bank_name = models.CharField(max_length=250,null=True,blank=True)
    
    
    resume = models.FileField(null=True,blank=True,upload_to='resume')
    educational_certificates = models.FileField(null=True,blank=True,upload_to='educational_certificates')
    professional_certifications = models.FileField(null=True,blank=True,upload_to='professional_certifications')
    offer_letter = models.FileField(null=True,blank=True, upload_to='offer_letter')
    identity_proof = models.FileField(null=True,blank=True, upload_to='identity_proof')
    utility_bills = models.FileField(null=True,blank=True, upload_to='utility_bills')
    experience_certificate = models.FileField(null=True,blank=True, upload_to='experience_certificate')

    work_experience = models.TextField(null=True,blank=True)
    skills = models.CharField(max_length=250,null=True,blank=True)
    languages = models.CharField(max_length=250,null=True,blank=True)
    hobbies = models.CharField(max_length=250,null=True,blank=True)
    linkedin_profile = models.CharField(max_length=250,null=True,blank=True)
    professional_references = models.CharField(max_length=250,null=True,blank=True)




    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email
    

