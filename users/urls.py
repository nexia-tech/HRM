from django.urls import path
from users.views import loginView,index, logout_view, edit_profile


urlpatterns = [
    path('',index,name='index'),
    path('login/',loginView,name='login'),
    path('logout/',logout_view,name='logout'),
    path('edit-profile/',edit_profile,name='edit-profile'),
]


