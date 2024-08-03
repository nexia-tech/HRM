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
    