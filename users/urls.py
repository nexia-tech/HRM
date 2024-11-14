from django.urls import path
from users.views import loginView, index, logout_view, edit_profile, create_employee_account, employees, employee_delete, view_profile, update_profile, create_account, update_user


urlpatterns = [
    path('', index, name='index'),
    path('login/', loginView, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('create-employee-account/', create_employee_account,
         name='create-employee-account'),
    path("employees/", employees, name='employees'),
    path("view-profile/<int:id>",view_profile,name='view-profile'),
    path('employee-delete/<int:id>/',employee_delete,name='employee-delete'),
    path("update-profile/<int:id>",update_profile,name='update-profile'),
    path("api/update-user/<int:user_id>/",update_user,name='update-user'),
    
    path("create-account/",create_account,name='create-account')

]

