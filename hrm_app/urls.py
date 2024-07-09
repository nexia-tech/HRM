from django.urls import path
from hrm_app.views import UpdateTimeRecords


urlpatterns = [
    path('update-time-record/',UpdateTimeRecords.as_view(),name='update-time-record'),
]


