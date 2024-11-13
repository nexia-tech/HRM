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
    position_applied_for = models.CharField(max_length=200,null=True,blank=True)
    father_name = models.CharField(max_length=200,null=True,blank=True)
    email_address = models.CharField(max_length=200,unique=True)
    cnic = models.CharField(max_length=200,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    marital_status = models.CharField(max_length=200,null=True,blank=True)
    expected_salary = models.CharField(max_length=200,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    contact_number = models.CharField(max_length=200,null=True,blank=True)
    other_mobile_number = models.CharField(max_length=200,null=True,blank=True)
    
    emergeny_contact_number = models.CharField(max_length=200,null=True,blank=True)
    emergency_contact_relation = models.CharField(max_length=200,null=True,blank=True)
    gender = models.CharField(max_length=200,null=True,blank=True)
    when_join_us = models.CharField(max_length=200,null=True,blank=True)
    shift_availablity = models.JSONField(null=True,blank=True)
    matric_details = models.JSONField(null=True,blank=True)
    intermediate_details = models.JSONField(null=True,blank=True)
    bachelors_details = models.JSONField(null=True,blank=True)
    masters_details = models.JSONField(null=True,blank=True)
    phd_details = models.JSONField(null=True,blank=True)
    diploma_details = models.JSONField(null=True,blank=True)
    job_experience = models.JSONField(null=True,blank=True)
    upload_profile = models.FileField(upload_to='profile-picture',null=True,blank=True)
    resume = models.FileField(upload_to='resume',null=True,blank=True)
    declaration = models.BooleanField(default=False) 
    is_employee = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True,blank=True)
    shortlisted_date = models.DateField(null=True,blank=True)
    rejected_reason = models.TextField(null=True,blank=True)
    remarks = models.TextField(null=True,blank=True)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)    
    
    
    def __str__(self):
        return self.name
    
    
class SystemAttendanceModel(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shift_date = models.DateField()
    shift_start_time = models.TimeField(null=True)
    time_out_time = models.TimeField(null=True, blank=True)
    remaining_hours = models.DurationField(null=True, blank=True)  # Leave default empty here
    is_present = models.BooleanField(default=True) 
    is_time_out_marked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)   
    
    def __str__(self):
        return self.employee.email
    
    def employee_hour(self):
        return self.employee.shift_duration_hours

    def save(self, *args, **kwargs):
        # Set remaining_hours default to employee's shift duration if not provided
        if self.remaining_hours is None and hasattr(self.employee, 'shift_duration_hours'):
            self.remaining_hours = timezone.timedelta(hours=self.employee.shift_duration_hours)
        super().save(*args, **kwargs)
        
        
    
    
class ThumbAttendnace(models.Model):
    employee = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.CharField(max_length=200,null=True,blank=True)
    time_table = models.CharField(max_length=200,null=True,blank=True)
    auto_assign = models.CharField(max_length=200,null=True,blank=True)
    on_duty = models.CharField(max_length=200)
    off_duty = models.CharField(max_length=200)
    clock_in = models.CharField(max_length=200,null=True,blank=True)
    clock_out = models.CharField(max_length=200,null=True,blank=True)
    normal = models.CharField(max_length=200,null=True,blank=True)
    real_time = models.CharField(max_length=200,null=True,blank=True)
    late = models.CharField(max_length=200,null=True,blank=True)
    early = models.CharField(max_length=200,null=True,blank=True)
    absent = models.CharField(max_length=200,null=True,blank=True)
    ot_time = models.CharField(max_length=200,null=True,blank=True)
    work_time = models.CharField(max_length=200,null=True,blank=True)
    exception = models.CharField(max_length=200,null=True,blank=True)
    must_cin =models.BooleanField(default=False)
    must_cout =models.BooleanField(default=False)
    department = models.CharField(max_length=200,null=True,blank=True)
    ndays = models.CharField(max_length=200,null=True,blank=True)
    weekend = models.CharField(max_length=200,null=True,blank=True)
    holiday = models.CharField(max_length=200,null=True,blank=True)
    att_time = models.TimeField(null=True,blank=True)
    ndays_ot = models.CharField(max_length=200,null=True,blank=True)
    weekend_ot = models.CharField(max_length=200,null=True,blank=True)
    holiday_ot = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.employee.email