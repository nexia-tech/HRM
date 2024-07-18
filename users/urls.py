from django.urls import path
from users.views import loginView, index, logout_view, edit_profile, create_employee_account, employees, employee_delete


urlpatterns = [
    path('', index, name='index'),
    path('login/', loginView, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('create-employee-account/', create_employee_account,
         name='create-employee-account'),
    path("employees/", employees, name='employees'),
    path('employee-delete/<int:id>/',employee_delete,name='employee-delete'),

]
