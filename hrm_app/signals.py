from django.db.models.signals import post_save
from django.dispatch import receiver
from hrm_app.models import ApplicantDetails, ApplicantHistory
from users.models import User
from datetime import datetime
from users.services import generate_password
import requests, json
from django.conf import settings

@receiver(post_save,sender=ApplicantDetails)
def create_employee_account(sender,created,instance,*args,**kwargs):
    # return
    if instance.is_employee:
        last_employee = User.objects.all().order_by('-employee_id').first()
        employee_id = int(last_employee.employee_id.split("-")[1]) + 1
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
    

@receiver(post_save, sender=ApplicantDetails)
def send_data_to_new_hrm(sender, instance: ApplicantDetails, created, **kwargs):
    # if not created:
    #     return
    print(instance.matric_details)
    try:
        data = {
            "name": instance.name,
            "email": instance.email_address,
            "mobile": instance.contact_number,
            "dob": instance.date_of_birth,
            "gender": instance.gender,
            "address": instance.address,
            "country": None,
            "state": None,
            "city": None,
            "zip": None,
            "cnic": instance.cnic,
            "father_name": instance.father_name,
            "marital_status": instance.marital_status,
            "expected_salary": instance.expected_salary,
            "contact_number": instance.contact_number,
            "other_mobile_number": instance.other_mobile_number,
            "emergeny_contact_number": instance.emergeny_contact_number,
            "emergency_contact_relation": instance.emergency_contact_relation,
            "when_join_us": instance.when_join_us,
            "shift_availablity": json.dumps(instance.shift_availablity),
            "matric_details": json.dumps(instance.matric_details),
            "intermediate_details": json.dumps(instance.intermediate_details),
            "bachelors_details": json.dumps(instance.bachelors_details),
            "masters_details": json.dumps(instance.masters_details),
            "phd_details": json.dumps(instance.phd_details),
            "diploma_details": json.dumps(instance.diploma_details),
            "job_experience": json.dumps(instance.job_experience),
            "declaration": instance.declaration,
            "is_employee": instance.is_employee,
            "follow_up_date": instance.follow_up_date,
            "shortlisted_date": instance.shortlisted_date,
            "rejected_reason": instance.rejected_reason,
            "remarks": instance.remarks,
            "status": instance.status,
            "is_rejected": instance.is_rejected,
            "is_scheduled": instance.is_scheduled,
            "scheduled_date": instance.scheduled_date,
            "scheduled_time": instance.scheduled_time,
            # "recruitment_id": 1,
            # "job_position_id": 1,
            # "stage_id": 1,
            "start_onboard": False,
            "hired": False,
            "canceled": False,
            "converted": False,
            "offer_letter_status": "not_sent",
            "source": "application"
        }

        base_url = settings.NEW_HRM_BASE_URL
        response = requests.post(f"{base_url}recruitment/api/candidates/", json=data,data=data)
        print("Candidate API Response:", response.status_code, response.json())
    
    except Exception as e:
        print("Error sending candidate data:", str(e))