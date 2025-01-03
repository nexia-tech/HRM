from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from users.models import User, Department, Role
from django.contrib.auth.decorators import login_required
from hrm_app.models import AttendanceModel, SystemAttendanceModel
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from core.models import ConfigurationModel, Ips
import requests, json, pytz
from users.services import generate_password
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import logging

BASE_URL = settings.BASE_URL
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s- %(asctime)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S",filename='log/users_app.log')


@login_required(login_url='login')
def index(request):
    user = request.user
    configuration = ConfigurationModel.objects.first()

#    # Get the current time in UTC
#     utc_now = datetime.utcnow()

#     # Specify the timezone you want to convert to
#     tz = pytz.timezone('Asia/Karachi')

#     # Convert UTC time to the specified timezone
#     karachi_time = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)

#     # Format the time as HH:MM:SS string
#     karachi_time_str = karachi_time.strftime("%H:%M:%S")

#     # Convert string to datetime object
#     datetime_obj = datetime.strptime(karachi_time_str, "%H:%M:%S")

#     # Extract time part and convert to 12-hour format
#     # current_time_12hr = datetime_obj.strftime("%I:%M:%S")

#     # Create timedelta object representing shift duration (8 hours in this example)
#     shift_duration_timedelta = timedelta(hours=user.shift_duration_hours)

    current_date = timezone.now().date()
#     attendance_records = AttendanceModel.objects.filter(
#         employee=user).order_by('shift_date')
#     attendance_obj = attendance_records.filter(
#         shift_date=current_date).first()
#     last_record = attendance_records.filter(is_time_out_marked=True).last()
#     try:
#         while last_record.shift_date < current_date:
#             next_date = last_record.shift_date + timedelta(days=1)
#             if next_date != current_date:
#                 attendance_object,isNotexist= AttendanceModel.objects.get_or_create(
#                     employee=user,
#                     shift_date=next_date,
#                     shift_time=None,
#                     remaining_hours=shift_duration_timedelta,
#                     is_present=False,
#                     is_time_out_marked=True
#                 )
#                 if not isNotexist:
#                     attendance_object.is_present=False
                    
#                 attendance_object.save()
#             last_record.shift_date = next_date

#     except Exception as e:
#         pass

#     if attendance_obj is None:
#         attendance_object = AttendanceModel()
#         attendance_object.employee = user
#         attendance_object.shift_date = current_date
#         attendance_object.shift_time = datetime_obj
#         attendance_object.remaining_hours = shift_duration_timedelta
#         attendance_object.save()
    
    context = {
        'user': user,
        'BASE_URL': settings.BASE_URL,
        "configuration": configuration,
    }
    return render(request, 'index.html', context)


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page (e.g., home)
                current_date = timezone.now().date()
                # Get the current time in UTC
                utc_now = datetime.utcnow()

                # Specify the timezone you want to convert to
                tz = pytz.timezone('Asia/Karachi')

                # Convert UTC time to the specified timezone
                karachi_time = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)

                # Format the time as HH:MM:SS string
                karachi_time_str = karachi_time.strftime("%H:%M:%S")

                # Convert string to datetime object
                datetime_obj = datetime.strptime(karachi_time_str, "%H:%M:%S")

                # Extract time part and convert to 12-hour format
                # current_time_12hr = datetime_obj.strftime("%I:%M:%S")

                # Create timedelta object representing shift duration (8 hours in this example)
                shift_duration_timedelta = timedelta(
                    hours=user.shift_duration_hours)

                # attendance_obj= AttendanceModel.objects.filter(employee=user,shift_date=current_date,is_time_out_marked=False).first()

                # last_record = AttendanceModel.objects.filter(employee=user,is_time_out_marked=True).last()

                attendance_records = AttendanceModel.objects.filter(
                    employee=user).order_by('-shift_date')
                attendance_obj = attendance_records.filter(
                    shift_date=current_date).first()
                last_record = attendance_records.filter(
                    is_time_out_marked=True).last()
                
                if last_record:
                    print("Last record shift_date:", last_record.shift_date)
                    print("Type of shift_date:", type(last_record.shift_date))
                    try:
                        while last_record.shift_date < current_date:
                            next_date = last_record.shift_date + timedelta(days=1)
                            if next_date != current_date:
                                try:
                                    attendance_object= AttendanceModel.objects.filter(
                                        employee=user,
                                        shift_date=next_date,
                                        shift_time=None,
                                        remaining_hours=shift_duration_timedelta,
                                        is_present=False,
                                        is_time_out_marked=True
                                    ).first()
                                    if attendance_object:
                                        attendance_object.is_present=False
                                        attendance_object.save()
                                except Exception as e:
                                    logging.ERROR(str(e))
                            last_record.shift_date = next_date

                    except Exception as e:
                        logging.ERROR(str(e))


                if attendance_obj is None:
                    attendance_object = AttendanceModel(
                        employee=user,
                        shift_date=current_date,
                        shift_time=datetime_obj,
                        remaining_hours=shift_duration_timedelta
                    )
                    attendance_object.save()

                # Replace 'home' with your desired URL name
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    data = {
        "email": request.user.email
    }
    break_request = requests.post(
        f"http://ec2-34-226-12-37.compute-1.amazonaws.com/hrm/break-time-record/", json=data)
    time_out_request = requests.post(
        f"http://ec2-34-226-12-37.compute-1.amazonaws.com/hrm/time-out/", json=data)
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def edit_profile(request):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    user = request.user
    context = {
        'user': user
        
    }
    return render(request, 'edit-profile.html', context)

def update_user(request,user_id):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)

        for field, value in data.items():
            if hasattr(user, field):
                if (field == 'doj' and value != "") or (field == 'dob' and value != "") or (field == 'shift_timings' and value != ""):
                    setattr(user, field, value)

        user.save()
        return JsonResponse({"success": True})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required(login_url='login')
def create_employee_account(request):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    if request.user.is_staff:
        departments = Department.objects.all()
        context = {
            'departments': departments
        }
        if request.method == 'POST':
            data = request.POST
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            designation = data.get('designation')
            father_name = data.get('father_name')
            email = data.get('email_address')
            company_email = data.get('company_email_address')
            nic = data.get('cnic')
            dob = data.get('date_of_birth')
            gender = data.get('gender')
            marital_status = data.get('marital_status')
            address = data.get('address')
            phone = data.get('phone')
            other_mobile_number = data.get('other_mobile_number')
            emergency_contact_person_phone = data.get('emergency_contact_number')
            supervisor_name = data.get('supervisor_name')
            professional_references = data.get('references')
            skills = data.get('skills')
            languages = data.get('languages')
            shift_timing = data.get('shift_timing')
            shift_end_timing = data.get('shift_end_timing')
            department = data.get('department')
            
           
            matric_details = {}
            intermediate_details = {}
            bachelors_details = {}
            masters_details = {}
            phd_details = {}
            diploma_details = {}

            matric_details['institute'] = data.get('matric_institute', None)
            matric_details['degree'] = data.get('matric_degree', None)
            matric_details['percentage'] = data.get('matric_grade', None)
            matric_details['year_passing'] = data.get(
                'matric_passing_year', None)

            intermediate_details['institute'] = data.get('intermediate_institute', None)
            intermediate_details['degree'] = data.get('intermediate_degree', None)
            intermediate_details['percentage'] = data.get('intermediate_grade', None)
            intermediate_details['year_passing'] = data.get('intermediate_passing_year', None)

            bachelors_details['institute'] = data.get('bachelors_institute', None)
            bachelors_details['degree'] = data.get('bachelors_degree', None)
            bachelors_details['percentage'] = data.get('bachelors_grade', None)
            bachelors_details['year_passing'] = data.get('bachelors_year_passing', None)

            masters_details['institute'] = data.get('masters_institute', None)
            masters_details['degree'] = data.get('masters_degree', None)
            masters_details['percentage'] = data.get('masters_grade', None)
            masters_details['year_passing'] = data.get('masters_year_passing', None)

            phd_details['institute'] = data.get('phsign-up-report/d_institute', None)
            phd_details['degree'] = data.get('phd_degree', None)
            phd_details['percentage'] = data.get('phd_grade', None)
            phd_details['year_passing'] = data.get('phd_year_passing', None)

            diploma_details['institute'] = data.get('diploma_institute', None)
            diploma_details['degree'] = data.get('diploma_degree', None)
            diploma_details['percentage'] = data.get('diploma_grade', None)
            diploma_details['year_passing'] = data.get('diploma_year_passing', None)

            current_salary = request.POST.get('current_salary')
            fuel_allowance = request.POST.get('fuel_allowance')
            other_allowance = request.POST.get('other_allowance')
            bank_name = request.POST.get('bank_name')
            
            password = generate_password()
          


            profile_picture = request.FILES.get('profile_picture')
            resume = request.FILES.get('resume')
            educational_certificates = request.FILES.get('educational_certificates')
            professional_certifications = request.FILES.get('professional_certifications')
            offer_letter = request.FILES.get('offer_letter')
            identity_proof = request.FILES.get('identity_proof')
            utility_bills = request.FILES.get('utility_bills')

            work_experience = request.POST.get('work_experience')
            hobbies = request.POST.get('hobbies')
            linkedin_profile = request.POST.get('linkedin_profile')
            working_hours = request.POST.get('shift_duration')
            doj = request.POST.get('date_of_joining')
            
            name = f"{first_name} {last_name}"
            depart = Department.objects.filter(name=department).first()
            user = User()
            user.username = email
            user.personal_email = email
            user.phone = phone
            user.name = name
            user.designation = designation
            user.department = depart
            user.matric_details = matric_details
            user.intermediate_details = intermediate_details
            user.masters_details == masters_details
            user.bachelors_details = bachelors_details
            user.masters_details = masters_details
            user.phd_details = phd_details
            user.diploma_details = diploma_details
            
            user.shift_end_timing = shift_end_timing
            user.active_password = password

            if working_hours != '':
                user.shift_duration_hours = working_hours
            user.is_staff = True

            if dob != "":
                user.dob = dob
            if doj != '':
                user.doj = doj
            user.gender = gender
            user.martial_status = marital_status
            user.cnic = nic
            user.address = address

            user.company_email = company_email

            user.emergency_contact_name = emergency_contact_person_phone
            user.emergency_contact_number = emergency_contact_person_phone

            if shift_timing != '':
                user.shift_timings = shift_timing

            user.supervisor_name = supervisor_name
            
            user.bank_name = bank_name
            user.basic_salary = current_salary
            user.fuel_allowance = fuel_allowance
            user.other_allowance = other_allowance

            user.profile_picture = profile_picture
            user.resume = resume
            user.educational_certificates = educational_certificates
            user.professional_certifications = professional_certifications
            user.offer_letter = offer_letter
            user.identity_proof = identity_proof
            user.utility_bills = utility_bills

            user.work_experience = work_experience
            user.skills = skills
            user.languages = languages
            user.hobbies = hobbies
            user.linkedin_profile = linkedin_profile
            user.professional_references = professional_references
            user.set_password(password)
            try:
                user.save()
                messages.success(request, 'Employee Account Has Been Created')
                return redirect('index')
            except Exception as e:
                logging.ERROR(str(e))
                print(e)
                messages.error(request, f"Error: {str(e)}")
                return redirect('create-employee-account')
        
        for role in request.user.roles.all():
            if role and not role.employee_view_access and not role.employee_add_access:
                messages.error(request, "You don't have permission")
                return redirect('index')
        return render(request, 'create-employee-account.html', context)
    else:
        return redirect('index')


@login_required(login_url='login')
def employees(request):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    employees = User.objects.all()
    context = {
        'employees': employees,
        'employee_edit_access':False
    }
    for role in request.user.roles.all():
        if role and not role.employee_view_access:
            messages.error(request, "You don't have permission")
            return redirect('index')
        else:
            if role.employee_edit_access:
                context['employee_edit_access'] = True
                
        return render(request, 'employees.html', context)
    messages.error(request, "You don't have permission")
    return redirect('index')


@login_required(login_url='login')
def view_profile(request):
    employee = request.user
    
     # Check if any field is None or an empty string
    any_field_empty = any(
        getattr(employee, field.name) in [None, '']  # Check for None or empty string
        for field in employee._meta.fields
    )
    context = {
        'employee': employee,
        "any_field_empty":any_field_empty
    }
    return render(request, 'view-profile.html', context)


@login_required(login_url='login')
def update_profile(request, id):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    user = User.objects.get(id=id)
    
     # Check if any field is None or an empty string
    any_field_empty = any(
        getattr(user, field.name) in [None, '']  # Check for None or empty string
        for field in user._meta.fields
    )
    context = {
        'user1': user,
        "any_field_empty":any_field_empty,
        'employee_edit_access':False
    }
    
    for role in request.user.roles.all():
        if role and not role.employee_view_access:
            messages.error(request, "You don't have permission")
            return redirect('index')
        else:
            if role.employee_edit_access:
                context['employee_edit_access'] = True
    
    if request.method == 'POST':
        email = request.POST.get('email')
        employee_id = request.POST.get('employee_id')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        dob = request.POST.get('dob', employee.dob)
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')
        nic = request.POST.get('nic')
        address = request.POST.get('address')
        company_email = request.POST.get('company_email')
        company_phone = request.POST.get('company_phone')
        emergency_contact_person_name = request.POST.get(
            'emergency_contact_person_name')
        emergency_contact_person_phone = request.POST.get(
            'emergency_contact_person_phone')
        realtionship_emergency_person = request.POST.get(
            'realtionship_emergency_person')

        designation = request.POST.get('designation')
        working_hours = request.POST.get('working_hours')
        employment_status = request.POST.get('employment_status')
        supervisor_name = request.POST.get('supervisor_name')
        job_description = request.POST.get('job_description')

        school_name = request.POST.get('school_name')
        school_city = request.POST.get('school_city')
        school_year_graduation = request.POST.get('school_year_graduation')
        school_major_subject = request.POST.get('school_major_subject')
        school_grade = request.POST.get('school_grade')

        college_name = request.POST.get('college_name')
        college_city = request.POST.get('college_city')
        college_year_graduation = request.POST.get('college_year_graduation')
        college_major_subject = request.POST.get('college_major_subject')
        college_grade = request.POST.get('college_grade')

        undergraduate_name = request.POST.get('undergraduate_name')
        undergraduate_city = request.POST.get('undergraduate_city')
        undergraduate_degree = request.POST.get('undergraduate_degree')
        undergraduate_major_subject = request.POST.get(
            'undergraduate_major_subject')
        undergraduate_graduation_year = request.POST.get(
            'undergraduate_graduation_year')
        undergraduate_grade = request.POST.get('undergraduate_grade')

        master_name = request.POST.get('master_name')
        master_city = request.POST.get('master_city')
        master_graduation_year = request.POST.get('master_graduation_year')
        master_major_subject = request.POST.get('master_major_subject')
        master_grade = request.POST.get('master_grade')
        master_degree = request.POST.get('master_degree')

        phd_name = request.POST.get('phd_name')
        phd_city = request.POST.get('phd_city')
        phd_degree = request.POST.get('phd_degree')
        phd_major_subject = request.POST.get('phd_major_subject')
        phd_graduation_year = request.POST.get('phd_graduation_year')
        phd_dissertation = request.POST.get('phd_dissertation')
        phd_supervisor = request.POST.get('phd_supervisor')

        basic_salary = request.POST.get('basic_salary')
        fuel_allowance = request.POST.get('fuel_allowance')
        other_allowance = request.POST.get('other_allowance')
        bank_name = request.POST.get('bank_name')

        profile_picture = request.FILES.get(
            'profile_picture', employee.profile_picture)
        resume = request.FILES.get('resume', employee.resume)
        educational_certificates = request.FILES.get(
            'educational_certificates', employee.educational_certificates)
        professional_certifications = request.FILES.get(
            'professional_certifications', employee.professional_certifications)
        offer_letter = request.FILES.get('offer_letter', employee.offer_letter)
        identity_proof = request.FILES.get(
            'identity_proof', employee.identity_proof)
        utility_bills = request.FILES.get(
            'utility_bills', employee.utility_bills)

        work_experience = request.POST.get('work_experience')
        skills = request.POST.get('skills')
        languages = request.POST.get('languages')
        hobbies = request.POST.get('hobbies')
        linkedin_profile = request.POST.get('linkedin_profile')
        professional_references = request.POST.get('professional_references')

        depart = Department.objects.filter(name=department).first()
        employee.username = email
        employee.email = email
        employee.phone = phone
        employee.name = name
        employee.designation = designation
        employee.department = depart

        if working_hours != '':
            employee.shift_duration_hours = working_hours
        employee.is_staff = True

        if dob != "":
            employee.dob = dob
        employee.employee_id = employee_id
        employee.gender = gender
        employee.martial_status = marital_status
        employee.cnic = nic
        employee.address = address

        employee.company_email = company_email
        employee.company_phone_number = company_phone

        employee.emergency_contact_name = emergency_contact_person_name
        employee.emergency_contact_number = emergency_contact_person_phone
        employee.emergency_contact_relationship = realtionship_emergency_person
        employee.employment_status = employment_status
        employee.supervisor_name = supervisor_name
        employee.job_description = job_description

        employee.schoool_name = school_name
        employee.school_city = school_city
        employee.school_grade = school_grade
        employee.school_major_subject = school_major_subject
        employee.school_year_graduation = school_year_graduation

        employee.college_name = college_name
        employee.college_city = college_city
        employee.college_year_graduation = college_year_graduation
        employee.college_grade = college_grade
        employee.college_major_subject = college_major_subject

        employee.undergraduate_name = undergraduate_name
        employee.undergraduate_city = undergraduate_city
        employee.undergraduate_degree = undergraduate_degree
        employee.undergraduate_grade = undergraduate_grade
        employee.undergraduate_graduation_year = undergraduate_graduation_year
        employee.undergraduate_major_subject = undergraduate_major_subject

        employee.master_name = master_name
        employee.master_city = master_city
        employee.master_degree = master_degree
        employee.master_grade = master_grade
        employee.master_graduation_year = master_graduation_year
        employee.master_major_subject = master_major_subject

        employee.phd_name = phd_name
        employee.phd_city = phd_city
        employee.phd_degree = phd_degree
        employee.phd_dissertation = phd_dissertation
        employee.phd_graduation_year = phd_graduation_year
        employee.phd_major_subject = phd_major_subject
        employee.phd_supervisor = phd_supervisor

        employee.bank_name = bank_name
        employee.basic_salary = basic_salary
        employee.fuel_allowance = fuel_allowance
        employee.other_allowance = other_allowance

        employee.profile_picture = profile_picture
        employee.resume = resume
        employee.educational_certificates = educational_certificates
        employee.professional_certifications = professional_certifications
        employee.offer_letter = offer_letter
        employee.identity_proof = identity_proof
        employee.utility_bills = utility_bills

        employee.work_experience = work_experience
        employee.skills = skills
        employee.languages = languages
        employee.hobbies = hobbies
        employee.linkedin_profile = linkedin_profile
        employee.professional_references = professional_references

        try:
            employee.save()
            messages.success(request, 'Employee Details Has Been Updated')
            return redirect('index')
        except Exception as e:
            logging.ERROR(str(e))
            
            messages.error(request, f"Error: {str(e)}")
            return redirect('update-profile', id=employee.id)

    else:
        return render(request, 'edit-profile.html', context)


@login_required(login_url='login')
def employee_delete(request, id):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request, 'Record has been deleted')

    return redirect('employees')

@csrf_exempt
def update_education(request,user_id):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(id=user_id)  # Adjust based on how you retrieve the user object
        # Update education fields based on keys
        for key, value in data.items():
            if key.startswith("matric_details_"):
                field = key.split("_", 2)[2]  # Extract field name (e.g., 'institute', 'degree')
                user.matric_details[field] = value
            elif key.startswith("intermediate_details_"):
                field = key.split("_", 2)[2]
                user.intermediate_details[field] = value
            elif key.startswith("bachelors_details_"):
                field = key.split("_", 2)[2]
                user.bachelors_details[field] = value
            elif key.startswith("masters_details_"):
                field = key.split("_", 2)[2]
                user.masters_details[field] = value
            elif key.startswith("phd_details_"):
                field = key.split("_", 2)[2]
                user.phd_details[field] = value
            elif key.startswith("diploma_details_"):
                field = key.split("_", 2)[2]
                user.diploma_details[field] = value

        # Save the updated user object
        user.save()

        return JsonResponse({"message": "Education updated successfully.","success": True})

    return JsonResponse({"error": "Invalid request method.","success":False}, status=400)


def update_resume(request,id):
    if request.method == "POST":
        # Upload resume file
        resume = request.FILES.get('resume')  # Get the uploaded file

        if resume:
            user = get_object_or_404(User, id=id)  # Safely get the user or return a 404 error
            user.resume = resume
            user.save()

            print("Uploaded file:", resume)
            messages.success(request, 'uploaded successfully.')
        else:
            messages.error(request, 'No file uploaded. Please try again.')

        return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))

    messages.error(request, 'Invalid request method.')
    return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))


def education_certification(request,id):
    if request.method == "POST":
        # Upload resume file
        educational_certificates = request.FILES.get('educational_certificates')  # Get the uploaded file

        if educational_certificates:
            user = get_object_or_404(User, id=id)  # Safely get the user or return a 404 error
            user.educational_certificates = educational_certificates
            user.save()

            print("Uploaded file:", educational_certificates)
            messages.success(request, 'uploaded successfully.')
        else:
            messages.error(request, 'No file uploaded. Please try again.')

        return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))

    messages.error(request, 'Invalid request method.')
    return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))


def professional_certifications(request,id):
    if request.method == "POST":
        # Upload resume file
        professional_certifications = request.FILES.get('professional_certifications')  # Get the uploaded file

        if professional_certifications:
            user = get_object_or_404(User, id=id)  # Safely get the user or return a 404 error
            user.professional_certifications = professional_certifications
            user.save()

            print("Uploaded file:", professional_certifications)
            messages.success(request, 'uploaded successfully.')
        else:
            messages.error(request, 'No file uploaded. Please try again.')

        return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))

    messages.error(request, 'Invalid request method.')
    return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))


def offer_letter(request,id):
    if request.method == "POST":
        # Upload resume file
        offer_letter = request.FILES.get('offer_letter')  # Get the uploaded file

        if offer_letter:
            user = get_object_or_404(User, id=id)  # Safely get the user or return a 404 error
            user.offer_letter = offer_letter
            user.save()

            print("Uploaded file:", offer_letter)
            messages.success(request, 'uploaded successfully.')
        else:
            messages.error(request, 'No file uploaded. Please try again.')

        return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))

    messages.error(request, 'Invalid request method.')
    return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))



def identity_proof(request,id):
    if request.method == "POST":
        # Upload resume file
        identity_proof = request.FILES.get('identity_proof')  # Get the uploaded file

        if identity_proof:
            user = get_object_or_404(User, id=id)  # Safely get the user or return a 404 error
            user.identity_proof = identity_proof
            user.save()

            print("Uploaded file:", identity_proof)
            messages.success(request, 'uploaded successfully.')
        else:
            messages.error(request, 'No file uploaded. Please try again.')

        return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))

    messages.error(request, 'Invalid request method.')
    return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))


def utility_bills(request,id):
    if request.method == "POST":
        # Upload resume file
        utility_bills = request.FILES.get('utility_bills')  # Get the uploaded file

        if utility_bills:
            user = get_object_or_404(User, id=id)  # Safely get the user or return a 404 error
            user.utility_bills = utility_bills
            user.save()

            print("Uploaded file:", utility_bills)
            messages.success(request, 'uploaded successfully.')
        else:
            messages.error(request, 'No file uploaded. Please try again.')

        return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))

    messages.error(request, 'Invalid request method.')
    return HttpResponseRedirect(reverse('update-profile',kwargs={'id':id}))


import pandas as pd
from django.http import JsonResponse

from datetime import datetime

def create_account(request):
    file = pd.read_excel('file.xlsx')
    records = list(file['name'])
    
    for index, name in enumerate(records):
        try:
            print(f"Processing {name}")
            row = file.iloc[index]
            
            employee_code = row['employee_id']
            phone = row['phone']
            name = row['name']
            first_name = row['first_name']
            last_name = row['last_name']
            father_name = row['father_name']
            martial_status = row['martial_status']
            father_name = row['father_name']
            father_name = row['father_name']
            father_name = row['father_name']
            
            
            joining_designation = row['joining_designation']
            designation = row['designation']
            joining_time_salary = row['joining_time_salary']
            
            department = row['department']
            personal_email = row['email']
            company_email = row['company_email'].lower()
            Emergencyno = row['emergency_contact_number']
            Address = row['address']
            doj = row['doj']
            dob = row['dob']
            
            print(f"Doj: {doj}")
            print(f"dob: {dob}")
            
            try:
                if isinstance(doj, str):
                    date_object = datetime.strptime(doj, '%m/%d/%Y')
                elif isinstance(doj, datetime):
                    date_object = doj
                else:
                    raise ValueError("Invalid type for doj")
                
                doj = date_object.strftime('%Y-%m-%d')
                
            except Exception as e:
                print(e)
                try:
                    date_object = datetime.strptime(doj, '%Y-%m-%d %H:%M:%S')
                    doj = date_object.strftime('%Y-%m-%d')
                except Exception as e:
                    print(e)
                
            try:
                if isinstance(dob, str):
                    date_object = datetime.strptime(dob, '%m/%d/%Y')
                elif isinstance(dob, datetime):
                    date_object = dob
                else:
                    raise ValueError("Invalid type for dob")
                
                dob = date_object.strftime('%Y-%m-%d')
                
            except Exception as e:
                print(e)
                try:
                    date_object = datetime.strptime(dob, '%Y-%m-%d %H:%M:%S')
                    dob = date_object.strftime('%Y-%m-%d')
                except Exception as e:
                    print(e)
            
            cnic = row['cnic']
            Basic_Salary = row['basic_salary']
            Fuel_Allowance = row['fuel_allowance']
            other_allowance = row['other_allowance']
            
            Bank_Details = row['bank_details']

            department = Department.objects.filter(name=department).first()
            user = User()  # Make sure you have imported User model
            password = generate_password()
            user.email = company_email
            user.personal_email = personal_email
            user.username = company_email
            user.name = name
            user.employee_id = employee_code
            user.active_password = password
            user.phone = phone
            user.designation = designation
            user.department = department
            user.cnic = cnic
            user.doj = doj
            user.other_allowance = other_allowance
            user.dob = dob
            user.joining_designation = joining_designation
            user.father_name = father_name
            user.first_name = first_name
            user.last_name = last_name
            user.martial_status = martial_status
            user.joining_time_salary = joining_time_salary
            user.basic_salary = Basic_Salary
            user.fuel_allowance = Fuel_Allowance
            user.bank_name = Bank_Details
            user.address = Address
            user.emergency_contact_number = Emergencyno
            user.company_email = company_email
            
            user.set_password(password)
            try:
                # Set the password properly
                user.save()
            except Exception as e:
                print(f"Errror: {e}")# Save the user object
        except Exception as e:
            logging.ERROR(str(e))
            
            print(f"Error for employee {name}: {e}")
        
    return JsonResponse({"message": "Script completed"})



@login_required(login_url='login')
def all_ips(request):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    if request.method == "POST":
        name = request.POST.get("name")
        ip_address = request.POST.get("ip")

        ip_instance = Ips.objects.filter(ip=ip_address).first()
        if ip_instance:  # Edit action
            ip_instance.name = name
            ip_instance.ip = ip_address
            ip_instance.save()
            messages.success(request,'Ip Updated successfully')
        else:  # Add action
            Ips.objects.create(name=name, ip=ip_address)
            messages.success(request,'Ip Added successfully')
        return redirect('all-ips')
    ips = Ips.objects.all().order_by('-created_at')
    params = {
        'ips':ips,
        'ip_add_access':False,
        'ip_delete_access':False
    }
    
    for role in request.user.roles.all():
        if role and not role.ip_view_access:
            messages.error(request, "You don't have permission")
            return redirect('index')
        else:
            params['ip_add_access'] = role.ip_add_access
            params['ip_delete_access'] = role.ip_delete_access
            
        return render(request, 'ips.html', params)
    messages.error(request, "You don't have permission")
    return redirect('index')

@login_required(login_url='login')
def delete_ip(request,id):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    if request.method == "DELETE":
        ip = get_object_or_404(Ips, id=id)
        ip.delete()
        messages.success(request, 'IP deleted successfully')
        return redirect('all-ips')
    
    
@login_required(login_url='login')
def view_roles(request):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    roles = Role.objects.all()
    employees = User.objects.all()
    params = {'roles':roles,'employees':employees}
    
    for role in request.user.roles.all():
        if role and not role.role_view_access:
            messages.error(request, "You don't have permission")
            return redirect('index')
        else:
            params['role_edit_access'] = role.role_edit_access
            params['role_delete_access'] = role.role_delete_access
            params['role_add_access'] = role.role_add_access
            
        return render(request, 'roles.html',params)
    messages.error(request, "You don't have permission")
    return redirect('index') 
    

@login_required(login_url='login')
def delete_role(request,id):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    if request.method == "DELETE":
        role = get_object_or_404(Role, id=id)
        role.delete()
        messages.success(request, 'Role deleted successfully')
        return redirect('view-roles')    




@login_required(login_url='login')
def create_role(request):
    
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    
    if request.method == "POST":
        name = request.POST.get('role_name')
        employee_view_access = True if request.POST.get("employee_view_access") == 'on' else False
        employee_add_access = True if request.POST.get("employee_add_access") == 'on'  else False
        employee_delete_access = True if request.POST.get("employee_delete_access") == 'on'  else False
        employee_edit_access = True if request.POST.get("employee_edit_access") == 'on'  else False
        ip_view_access = True if request.POST.get("ip_view_access") == 'on'  else False
        ip_add_access = True if request.POST.get("ip_add_access") == 'on'  else False
        ip_delete_access = True if request.POST.get("ip_delete_access") == 'on'  else False
        ip_edit_access = True if request.POST.get("ip_edit_access") == 'on'  else False
        role_view_access = True if request.POST.get("role_view_access") == 'on'  else False
        role_add_access = True if request.POST.get("role_add_access") == 'on'  else False
        role_delete_access = True if request.POST.get("role_delete_access") == 'on'  else False
        role_edit_access = True if request.POST.get("role_edit_access") == 'on'  else False
        applicant_view_access = True if request.POST.get("applicant_view_access") == 'on'  else False
        applicant_add_access = True if request.POST.get("applicant_add_access") == 'on'  else False
        applicant_delete_access = True if request.POST.get("applicant_delete_access") == 'on'  else False
        applicant_edit_access = True if request.POST.get("applicant_edit_access") == 'on'  else False
        
        Role.objects.create(
         name=name,employee_view_access=employee_view_access,employee_add_access=employee_add_access,employee_delete_access=employee_delete_access,employee_edit_access=employee_edit_access,ip_view_access=ip_view_access,ip_add_access=ip_add_access,ip_delete_access=ip_delete_access,ip_edit_access=ip_edit_access,role_view_access=role_view_access,
        role_add_access=role_add_access,role_edit_access=role_edit_access,role_delete_access=role_delete_access,applicant_view_access=applicant_view_access,applicant_add_access=applicant_add_access,applicant_delete_access=applicant_delete_access,applicant_edit_access=applicant_edit_access
        )
        messages.success(request, 'Role created successfully')
        
        return redirect('view-roles')
    fieldnames = [{'Employee':['employee_view_access','employee_add_access','employee_delete_access','employee_edit_access']},{'IP':['ip_view_access','ip_add_access','ip_delete_access','ip_edit_access']},{'role':['role_view_access','role_add_access','role_delete_access','role_edit_access']},{'Applicant':['applicant_view_access','applicant_add_access','applicant_delete_access','applicant_edit_access']}]

    params = {'fieldnames':fieldnames,'role_add_access':False}
    
    for role in request.user.roles.all():
        if role and not role.role_view_access:
            messages.error(request, "You don't have permission")
            return redirect('index')
        else:
            if role.role_add_access:
                params['role_add_access'] = True
                
    return render(request, 'create-role.html',params)
    
    
def add_permission(request,id):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    
    if request.method == "POST":
        emails = request.POST.getlist('emails')
        role = Role.objects.get(id=id)
        for email in emails:
            user = User.objects.filter(email=email).first()
            user.roles.add(role)
            user.save()
        messages.success(request, 'Permissions added successfully')
        return redirect('view-roles')
    
    
def view_group_employees(request,id):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    
    employees = User.objects.filter(roles__id=id)
    params = {'employees':employees}
    
    for role in request.user.roles.all():
        if role and not role.role_view_access:
            messages.error(request, "You don't have permission")
            return redirect('index')
        else:
            params['role_edit_access'] = role.role_edit_access
            params['role_delete_access'] = role.role_delete_access
            params['role_add_access'] = role.role_add_access
            
            
        return render(request,'view-group-employees.html',params)
    messages.error(request, "You don't have permission")
    return redirect('index')


def update_role(request,id):
    role = Role.objects.filter(id=id)
    
    
    if request.method == "POST":
        name = request.POST.get('role_name')
        employee_view_access = True if request.POST.get("employee_view_access") == 'on' else False
        employee_add_access = True if request.POST.get("employee_add_access") == 'on'  else False
        employee_delete_access = True if request.POST.get("employee_delete_access") == 'on'  else False
        employee_edit_access = True if request.POST.get("employee_edit_access") == 'on'  else False
        ip_view_access = True if request.POST.get("ip_view_access") == 'on'  else False
        ip_add_access = True if request.POST.get("ip_add_access") == 'on'  else False
        ip_delete_access = True if request.POST.get("ip_delete_access") == 'on'  else False
        ip_edit_access = True if request.POST.get("ip_edit_access") == 'on'  else False
        role_view_access = True if request.POST.get("role_view_access") == 'on'  else False
        role_add_access = True if request.POST.get("role_add_access") == 'on'  else False
        role_delete_access = True if request.POST.get("role_delete_access") == 'on'  else False
        role_edit_access = True if request.POST.get("role_edit_access") == 'on'  else False
        applicant_view_access = True if request.POST.get("applicant_view_access") == 'on'  else False
        applicant_add_access = True if request.POST.get("applicant_add_access") == 'on'  else False
        applicant_delete_access = True if request.POST.get("applicant_delete_access") == 'on'  else False
        applicant_edit_access = True if request.POST.get("applicant_edit_access") == 'on'  else False
        
        
        role.update(
            id=id,
        name=name,employee_view_access=employee_view_access,employee_add_access=employee_add_access,employee_delete_access=employee_delete_access,employee_edit_access=employee_edit_access,ip_view_access=ip_view_access,ip_add_access=ip_add_access,ip_delete_access=ip_delete_access,ip_edit_access=ip_edit_access,role_view_access=role_view_access,
        role_add_access=role_add_access,role_edit_access=role_edit_access,role_delete_access=role_delete_access,applicant_view_access=applicant_view_access,applicant_add_access=applicant_add_access,applicant_delete_access=applicant_delete_access,applicant_edit_access=applicant_edit_access)
        messages.success(request, 'Role permission updated successfully')
        
        return redirect('view-roles')

    fieldnames = [{'Employee':['employee_view_access','employee_add_access','employee_delete_access','employee_edit_access']},{'IP':['ip_view_access','ip_add_access','ip_delete_access','ip_edit_access']},{'role':['role_view_access','role_add_access','role_delete_access','role_edit_access']},{'Applicant':['applicant_view_access','applicant_add_access','applicant_delete_access','applicant_edit_access']}]
    params = {'fieldnames':fieldnames,'role':role.first(),'role_edit_access':False}
    
    for role in request.user.roles.all():
        if role and not role.role_view_access:
            messages.error(request, "You don't have permission")
            return redirect('index')
        else:
            if role.role_edit_access:
                params['role_edit_access'] = True


    return render(request,'update-role.html',params)
    
    
    