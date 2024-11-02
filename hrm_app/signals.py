from django.db.models.signals import post_save
from django.dispatch import receiver
from hrm_app.models import ApplicantDetails
from users.models import User
from datetime import datetime
from users.services import generate_password

@receiver(post_save,sender=ApplicantDetails)
def create_employee_account(sender,created,instance,*args,**kwargs):
    if instance.is_employee:
        print("working")
        user = User()
        user.name = instance.name
        user.username = instance.email_address
        user.email = instance.email_address
        user.cnic = instance.cnic
        user.address = instance.address
        user.doj = datetime.now().date()
        user.resume  = instance.resume
        user.profile_picture = instance.upload_profile
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