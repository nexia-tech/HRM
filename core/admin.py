from django.contrib import admin
from core.models import ConfigurationModel, Ips
from import_export.admin import ImportExportModelAdmin


admin.site.register(ConfigurationModel)

class IpsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','ip','active','created_at']
    search_fields =['name','ip',]
    list_filter = ['active','created_at']


admin.site.register(Ips, IpsAdmin)