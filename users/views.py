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
                try:
                    while last_record.shift_date < current_date:
                        next_date = last_record.shift_date + timedelta(days=1)
                        if next_date != current_date:
                            attendance_object,isNotexist= AttendanceModel.objects.get_or_create(
                                employee=user,
                                shift_date=next_date,
                                shift_time=None,
                                remaining_hours=shift_duration_timedelta,
                                is_present=False,
                                is_time_out_marked=True
                            )
                            if not isNotexist:
                                attendance_object.is_present=False
                                
                            attendance_object.save()
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
            email = request.POST.get('email')
            employee_id = request.POST.get('employee_id')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            department = request.POST.get('department')
            password = request.POST.get('password')
            dob = request.POST.get('dob')
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
            doj = request.POST.get('doj')
            shift_timing = request.POST.get('shift_timing')
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
            college_year_graduation = request.POST.get(
                'college_year_graduation')
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

            profile_picture = request.FILES.get('profile_picture')
            resume = request.FILES.get('resume')
            educational_certificates = request.FILES.get(
                'educational_certificates')
            professional_certifications = request.FILES.get(
                'professional_certifications')
            offer_letter = request.FILES.get('offer_letter')
            identity_proof = request.FILES.get('identity_proof')
            utility_bills = request.FILES.get('utility_bills')

            work_experience = request.POST.get('work_experience')
            skills = request.POST.get('skills')
            languages = request.POST.get('languages')
            hobbies = request.POST.get('hobbies')
            linkedin_profile = request.POST.get('linkedin_profile')
            professional_references = request.POST.get(
                'professional_references')

            depart = Department.objects.filter(name=department).first()
            user = User()
            user.username = email
            user.email = email
            user.phone = phone
            user.name = name
            user.designation = designation
            user.department = depart
            user.active_password = password

            if working_hours != '':
                user.shift_duration_hours = working_hours
            user.is_staff = True

            if dob != "":
                user.dob = dob
            if doj != '':
                user.doj = doj
            user.employee_id = employee_id
            user.gender = gender
            user.martial_status = marital_status
            user.cnic = nic
            user.address = address

            user.company_email = company_email
            user.company_phone_number = company_phone

            user.emergency_contact_name = emergency_contact_person_name
            user.emergency_contact_number = emergency_contact_person_phone
            user.emergency_contact_relationship = realtionship_emergency_person
            if shift_timing != '':
                user.shift_timings = shift_timing
            user.employment_status = employment_status
            user.supervisor_name = supervisor_name
            user.job_description = job_description

            user.schoool_name = school_name
            user.school_city = school_city
            user.school_grade = school_grade
            user.school_major_subject = school_major_subject
            user.school_year_graduation = school_year_graduation

            user.college_name = college_name
            user.college_city = college_city
            user.college_year_graduation = college_year_graduation
            user.college_grade = college_grade
            user.college_major_subject = college_major_subject

            user.undergraduate_name = undergraduate_name
            user.undergraduate_city = undergraduate_city
            user.undergraduate_degree = undergraduate_degree
            user.undergraduate_grade = undergraduate_grade
            user.undergraduate_graduation_year = undergraduate_graduation_year
            user.undergraduate_major_subject = undergraduate_major_subject

            user.master_name = master_name
            user.master_city = master_city
            user.master_degree = master_degree
            user.master_grade = master_grade
            user.master_graduation_year = master_graduation_year
            user.master_major_subject = master_major_subject

            user.phd_name = phd_name
            user.phd_city = phd_city
            user.phd_degree = phd_degree
            user.phd_dissertation = phd_dissertation
            user.phd_graduation_year = phd_graduation_year
            user.phd_major_subject = phd_major_subject
            user.phd_supervisor = phd_supervisor

            user.bank_name = bank_name
            user.basic_salary = basic_salary
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

def create_account(request):
    file = pd.read_excel('file.xlsx')
    records = list(file['name'])
    
    for index, name in enumerate(records):
        try:
            print(f"Processing {name}")
            row = file.iloc[index]
            
            employee_code = row['employee_id']
            phone = row['phone']
            designation = row['designation']
            department = row['department']
            personal_email = row['personal_email']
            official_email = row['official_email']
            Emergencyno = row['Emergencyno']
            Address = row['Address']
            doj = row['DOJ']
            cnic = row['CNIC']
            Basic_Salary = row['Basic_Salary']
            Fuel_Allowance = row['Fuel_Allowance']
            Bank_Details = row['Bank_Details']

            department = Department.objects.filter(name=department).first()
            user = User()  # Make sure you have imported User model
            password = generate_password()
            user.email = personal_email
            user.username = personal_email
            user.name = name
            user.employee_id = employee_code
            user.active_password = password
            user.phone = phone
            user.designation = designation
            user.department = department
            user.cnic = cnic
            user.doj = doj
            user.basic_salary = Basic_Salary
            user.fuel_allowance = Fuel_Allowance
            user.bank_name = Bank_Details
            user.address = Address
            user.emergency_contact_number = Emergencyno
            user.company_email = official_email
            
            user.set_password(password)  # Set the password properly
            user.save()                  # Save the user object
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
    