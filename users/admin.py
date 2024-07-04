from django.contrib import admin
from users.models import User, Department
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','phone']
    autocomplete_fields = ['department']
    filter_horizontal = ['user_permissions']

admin.site.register(User,UserAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']

admin.site.register(Department,DepartmentAdmin)