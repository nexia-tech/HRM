from django.urls import path
from users.views import loginView, index, logout_view, edit_profile, create_employee_account, employees, employee_delete, view_profile, update_profile, create_account, update_user, update_education, update_resume, education_certification, offer_letter, identity_proof, utility_bills, professional_certifications, all_ips, delete_ip, view_roles, delete_role, create_role, add_permission, view_group_employees


urlpatterns = [
    path('', index, name='index'),
    path('login/', loginView, name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit-profile/', edit_profile, name='edit-profile'),
    path('create-employee-account/', create_employee_account,
         name='create-employee-account'),
    path("employees/", employees, name='employees'),
    path("view-profile/",view_profile,name='view-profile'),
    path('employee-delete/<int:id>/',employee_delete,name='employee-delete'),
    path("update-profile/<int:id>",update_profile,name='update-profile'),
    path("api/update-user/<int:user_id>/",update_user,name='update-user'),
    
    path("create-account/",create_account,name='create-account'),
    path('update-education/<int:user_id>/', update_education, name='update_education'),
    path("update-resume/<int:id>/",update_resume,name='update-resume'),
    path("educational-certificates/<int:id>/",education_certification,name='educational-certificates'),
    path("offer-letter/<int:id>/",offer_letter,name='offer-letter'),
    path("identity-proof/<int:id>/",identity_proof,name='identity-proof'),
    path("utility-bills/<int:id>/",utility_bills,name='utility-bills'),
    path("professional-certifications/<int:id>/",professional_certifications,name='professional-certifications'),
    path("all-ips/",all_ips,name='all-ips'),
    path("delete-ips/<int:id>/",delete_ip,name='delete-ips'),
    path("view-roles/",view_roles,name='view-roles'),
    path("delete-role/<int:id>/",delete_role,name='delete-role'),
    path("create-role/",create_role,name='create-role'),
    path("add-permission/<int:id>/",add_permission,name='add-permission'),
    path("view-group-employees/<int:id>/",view_group_employees,name='view-group-employees'),
    

]

