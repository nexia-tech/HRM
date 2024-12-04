from django.contrib import admin
from users.models import User, Department, Role
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import AdminSite


admin.site.unregister(Group)

class HRMAdminSite(AdminSite):
    site_header = "HRM Admin"
    site_title = "HRM Admin"
    index_title = "HRM Admin"
    
hrm_admin = HRMAdminSite(name='hrm_admin')

class UserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['username','email','company_email','phone','shift_duration_hours','employee_id','created_at']
    autocomplete_fields = ['department']
    filter_horizontal = ['user_permissions']
    list_filter = ['department','gender','doj','dob']
    search_fields = ['name','email','username','phone','employee_id','company_email','company_phone_number','emergency_contact_name','emergency_contact_number','emergency_contact_relationship']
    filter_horizontal = ['roles']

admin.site.register(User,UserAdmin)

class DepartmentAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']

admin.site.register(Department,DepartmentAdmin)

admin.site.register(Role)



hrm_admin.register(User,UserAdmin)
hrm_admin.register(Department,DepartmentAdmin)
hrm_admin.register(Role)