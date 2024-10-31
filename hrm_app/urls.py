from django.urls import path
from hrm_app.views import UpdateTimeRecords, my_attendance, BreakTimeCalculate, break_time_stamp, TimeOut, StartThreadView, StopThreadView, employees_report, ApplicantDetailsAPI, ShiftStartTime, ShiftEndTime, thumbAttendance, applicants, applicant_detail, get_csrf_token


urlpatterns = [
    path('update-time-record/', UpdateTimeRecords.as_view(),
         name='update-time-record'),
    path('my-attendance/', my_attendance, name='my-attendance'),
    path('break-time-record/', BreakTimeCalculate.as_view(),
         name='break-time-record'),
    path('break-time-stamp/<int:id>/', break_time_stamp, name='break-time-stamp'),
    path('time-out/', TimeOut.as_view(), name='time-out'),

    path('start-timer-thread/', StartThreadView.as_view(), name='start_thread'),
    path('stop-timer-thread/', StopThreadView.as_view(), name='stop_thread'),
    path("employees-report/<int:id>/", employees_report, name='employees-report'),
    path('api/applicant/', ApplicantDetailsAPI.as_view(), name='applicant-api'),

    path('api/shift-start-time/', ShiftStartTime.as_view(), name='shift-start-time'),
    path('api/shift-end-time/', ShiftEndTime.as_view(), name='shift-end-time'),

    path("thumb-attendance/<int:id>/", thumbAttendance, name='thumb-attendance'),
    path('applicants/', applicants, name='applicants'),
    path('applicant/<int:id>/', applicant_detail, name='applicant'),
    path('api/get-csrf-token/', get_csrf_token, name='get-csrf-token'),

]
