from django.db import models
from users.models import User
from django.utils import timezone

class EmployeeBreakRecords(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    break_type = models.CharField(max_length=200,null=True,blank=True,default='System Generated')
    break_comments = models.TextField(null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    record_date = models.DateField(null=True,blank=True)
    is_break_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.employee.email

class AttendanceModel(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shift_date = models.DateField()
    shift_time = models.TimeField(null=True)
    working_hours = models.DurationField(default=timezone.timedelta(0))
    remaining_hours = models.DurationField(default=timezone.timedelta(hours=8))
    break_time_stamp = models.ManyToManyField(EmployeeBreakRecords,blank=True)
    break_hours = models.DurationField(default=timezone.timedelta(0))
    total_hours_completed = models.DurationField(default=timezone.timedelta(0))
    is_present = models.BooleanField(default=True) 
    time_out_time = models.TimeField(null=True,blank=True)
    is_time_out_marked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)   
    
    def __str__(self):
        return str(self.id)
    
    
class LeavesModel(models.Model):
    LEAVE_CHOICES = (
        ('Sick Leave','Sick Leave'),
        ('Earned Leave','Earned Leave'),
        ('Paid Leave','Paid Leave'),
        ('Casual Leave','Casual Leave'),
        ('Maternity Leave','Maternity Leave'),
        ('National Holiday','National Holiday'),
    )
    employee = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    leave_type = models.CharField(choices=LEAVE_CHOICES,max_length=200)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)    
    
    
    def __str__(self):
        return self.employee.email    
    
    
    
class ScreenShotRecords(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateField()
    s3_screen_shot_link = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.employee.email      
    
    
class ApplicantDetails(models.Model):
    name = models.CharField(max_length=200)
    position_applied_for = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200,unique=True)
    cnic = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=200)
    expected_salary = models.CharField(max_length=200)
    address = models.TextField()
    contact_number = models.CharField(max_length=200)
    emergeny_contact_number = models.CharField(max_length=200)
    when_join_us = models.CharField(max_length=200)
    shift_availablity = models.JSONField()
    matric_details = models.JSONField()
    intermediate_details = models.JSONField()
    bachelors_details = models.JSONField(null=True,blank=True)
    masters_details = models.JSONField(null=True,blank=True)
    phd_details = models.JSONField(null=True,blank=True)
    diploma_details = models.JSONField(null=True,blank=True)
    job_experience = models.JSONField()
    upload_profile = models.FileField(upload_to='profile-picture',null=True,blank=True)
    resume = models.FileField(upload_to='resume',null=True,blank=True)
    declaration = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)    
    
    
    def __str__(self):
        return self.name
    
    
class SystemAttendanceModel(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shift_date = models.DateField()
    shift_start_time = models.TimeField(null=True)
    time_out_time = models.TimeField(null=True,blank=True)
    remaining_hours = models.DurationField(default=timezone.timedelta(hours=8))
    is_present = models.BooleanField(default=True) 
    is_time_out_marked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)   
    
    def __str__(self):
        return self.employee.email