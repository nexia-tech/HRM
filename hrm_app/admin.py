from django.contrib import admin
from hrm_app.models import AttendanceModel, LeavesModel, EmployeeBreakRecords, ScreenShotRecords, ApplicantDetails, SystemAttendanceModel,ThumbAttendnace
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

class SystemAttendanceModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['employee','shift_date','shift_start_time','time_out_time','remaining_hours','is_present','is_time_out_marked','created_at']
    list_filter = ['is_present','is_time_out_marked','created_at']
    search_fields = ['employee__email','shift_date','shift_start_time','time_out_time','remaining_hours','is_present','is_time_out_marked','created_at'] 
    

admin.site.register(SystemAttendanceModel,SystemAttendanceModelAdmin)

class ThumbAttendnaceAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['employee','date','time_table','auto_assign','on_duty','created_at']
    search_fields = ['employee__email','date','time_table','auto_assign','on_duty']
    list_filter = ['date','time_table','created_at']
    autocomplete_fields = ['employee']
    
    
admin.site.register(ThumbAttendnace,ThumbAttendnaceAdmin)