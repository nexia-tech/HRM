from django.db.models.signals import post_save
from django.dispatch import receiver
from hrm_app.models import ApplicantDetails, ApplicantHistory
from users.models import User
from datetime import datetime
from users.services import generate_password

@receiver(post_save,sender=ApplicantDetails)
def create_employee_account(sender,created,instance,*args,**kwargs):
    return
    if instance.is_employee:
        print("working")
        last_employee = User.objects.all().order_by('-employee_id').first()
        print(last_employee.employee_id.split("-"))
        print(last_employee.employee_id.split("-")[1])
        employee_id = int(last_employee.employee_id.split("-")[1]) + 1
        print(employee_id)
        if employee_id < 100:
            employee_id = f"NX-0{str(employee_id)}"
        else:
            employee_id = f"NX-{str(employee_id)}"
        
        user = User()
        user.name = instance.name
        user.username = instance.email_address
        user.email = instance.email_address
        user.cnic = instance.cnic
        user.address = instance.address
        user.doj = datetime.now().date()
        user.resume  = instance.resume
        user.profile_picture = instance.upload_profile
        user.employee_id = employee_id
        password = generate_password()
        user.set_password(password)
        user.active_password = password
        user.emergency_contact_name = instance.emergency_contact_relation
        user.phone = instance.contact_number
        user.martial_status = instance.marital_status
        user.dob = instance.date_of_birth
        try:
            user.save()
            print("Done")
        except Exception as e:
            print(str(e))
            
            
@receiver(post_save,sender=ApplicantDetails)
def update_history(sender,created,instance, *args, **kwargs):
    history = ApplicantHistory()
    history.comment = instance.remarks or instance.rejected_reason
    history.status = instance.status
    history.user = instance.user
    history.applicant = instance
    history.date = instance.shortlisted_date or instance.follow_up_date or instance.scheduled_date
    history.save()