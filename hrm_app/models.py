from django.db import models
from users.models import User


class AttendanceModel(models.Model):
    employee = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    shift_date = models.DateField()
    shift_time = models.TimeField()
    working_hours = models.IntegerField(default=8)
    remainig_hours = models.IntegerField(default=8)
    break_hours = models.IntegerField(default=0)
    total_hours_completed = models.IntegerField(default=8)
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