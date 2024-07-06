from django.db import models
from users.models import User
from django.utils import timezone


class AttendanceModel(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    shift_date = models.DateField()
    shift_time = models.TimeField(null=True)
    working_hours = models.DurationField(default=timezone.timedelta(0))
    remaining_hours = models.DurationField(default=timezone.timedelta(hours=8))
    break_hours = models.DurationField(default=timezone.timedelta(0))
    total_hours_completed = models.DurationField(default=timezone.timedelta(0))
    created_at = models.DateTimeField(auto_now_add=True)   
    
    def __str__(self):
        return self.employee.email
    
    
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