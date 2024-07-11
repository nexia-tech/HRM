from django.urls import path
from hrm_app.views import UpdateTimeRecords, my_attendance, BreakTimeCalculate


urlpatterns = [
    path('update-time-record/',UpdateTimeRecords.as_view(),name='update-time-record'),
    path('my-attendance/',my_attendance,name='my-attendance'),
    path('break-time-record/',BreakTimeCalculate.as_view(),name='break-time-record'),
    
]

