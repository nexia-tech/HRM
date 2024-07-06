from django.urls import path
from users.views import loginView,index, logout_view, UpdateTimeRecords


urlpatterns = [
    path('',index,name='index'),
    path('login/',loginView,name='login'),
    path('logout/',logout_view,name='logout'),
    path('update-time-record/',UpdateTimeRecords.as_view(),name='update-time-record')
]


