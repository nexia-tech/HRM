from django.contrib import admin
from hrm_app.models import AttendanceModel, LeavesModel
from import_export.admin import ImportExportModelAdmin

class AttendanceModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['employee','shift_date','shift_time','working_hours','remaining_hours','break_hours','total_hours_completed','created_at']
    search_fields = ['employee__email']
    

admin.site.register(AttendanceModel,AttendanceModelAdmin)



# admin.site.register(LeavesModel)