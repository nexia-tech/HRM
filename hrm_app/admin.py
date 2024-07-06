from django.contrib import admin
from hrm_app.models import AttendanceModel, LeavesModel

class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ['employee','shift_date','shift_time','working_hours','remaining_hours','total_hours_completed','created_at']
    search_fields = ['employee__email']
    

admin.site.register(AttendanceModel,AttendanceModelAdmin)



admin.site.register(LeavesModel)