from django.urls import path
from hrm_app.views import UpdateTimeRecords, my_attendance


urlpatterns = [
    path('update-time-record/',UpdateTimeRecords.as_view(),name='update-time-record'),
    path('my-attendance/',my_attendance,name='my-attendance')
]


