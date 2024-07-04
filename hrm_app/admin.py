from django.contrib import admin
from hrm_app.models import AttendanceModel, LeavesModel

admin.site.register(AttendanceModel)
admin.site.register(LeavesModel)