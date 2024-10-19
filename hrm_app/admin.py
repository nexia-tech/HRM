from django.contrib import admin
from hrm_app.models import AttendanceModel, LeavesModel, EmployeeBreakRecords, ScreenShotRecords, ApplicantDetails, SystemAttendanceModel
from import_export.admin import ImportExportModelAdmin

class AttendanceModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['employee','shift_date','shift_time','working_hours','remaining_hours','break_hours','total_hours_completed','time_out_time','created_at']
    search_fields = ['employee__email']
    list_filter = ['employee__email','is_time_out_marked']
    filter_horizontal = ['break_time_stamp']
    autocomplete_fields = ['employee']
    

admin.site.register(AttendanceModel,AttendanceModelAdmin)

class EmployeeBreakRecordAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['employee','break_type','start_time','end_time','record_date','is_break_end']
    search_fields = ['employee__email']
    list_filter = ['employee__email','break_type','is_break_end']
    autocomplete_fields = ['employee']

admin.site.register(EmployeeBreakRecords,EmployeeBreakRecordAdmin)

admin.site.register(ScreenShotRecords)

class ApplicantDetailsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','email_address','cnic']
    search_fields = ['name','email_address']
    list_filter = ['marital_status','declaration','position_applied_for']

admin.site.register(ApplicantDetails,ApplicantDetailsAdmin)

admin.site.register(SystemAttendanceModel)