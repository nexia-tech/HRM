from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from users.models import User, Department
from django.contrib.auth.decorators import login_required
from hrm_app.models import AttendanceModel
from django.utils import timezone
from datetime import datetime,timedelta
import pytz
from django.conf import settings
from core.models import ConfigurationModel
    
@login_required(login_url='login')
def index(request):
    user = request.user
    configuration = ConfigurationModel.objects.first()

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
    shift_duration_timedelta = timedelta(hours=user.shift_duration_hours)
    
    
    
    current_date = timezone.now().date()
    attendance_obj= AttendanceModel.objects.filter(employee=user,shift_date=current_date,is_time_out_marked=False).first()

    
    if attendance_obj is None:
        attendance_object = AttendanceModel()
        attendance_object.employee = user
        attendance_object.shift_date = current_date
        attendance_object.shift_time = datetime_obj
        attendance_object.remaining_hours = shift_duration_timedelta
        attendance_object.save()
    
    
    context ={
        'user':user,
        'attendance_obj':attendance_obj,
        'BASE_URL':settings.BASE_URL,
        "configuration":configuration
    }
    return render(request,'index.html',context)


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
                shift_duration_timedelta = timedelta(hours=user.shift_duration_hours)
                

                attendance_obj= AttendanceModel.objects.filter(employee=user,shift_date=current_date,is_time_out_marked=False).first()

               
                if attendance_obj is None:
                    attendance_object = AttendanceModel()
                    attendance_object.employee = user
                    attendance_object.shift_date = current_date
                    attendance_object.shift_time = datetime_obj
                    attendance_object.remaining_hours = shift_duration_timedelta
                    attendance_object.save()
                    
                return redirect('index')  # Replace 'home' with your desired URL name
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        profile_picture = request.FILES.get('profile_picture')
        bio = request.POST.get('bio')
        user.phone = phone
        user.name = name
        user.bio = bio
        user.profile_picture = profile_picture
        user.save()
        messages.success(request,'Profile has been updated')
        return redirect('index')
    else:
        context = {
            'user':user
        }
        return render(request,'edit-profile.html',context)
    
    
@login_required(login_url='login')
def create_employee_account(request):
    if request.user.is_superuser:
        departments = Department.objects.all()
        context = {
            'departments':departments
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
            emergency_contact_person_name = request.POST.get('emergency_contact_person_name')
            emergency_contact_person_phone = request.POST.get('emergency_contact_person_phone')
            realtionship_emergency_person = request.POST.get('realtionship_emergency_person')
            
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
            college_year_graduation = request.POST.get('college_year_graduation')
            college_major_subject = request.POST.get('college_major_subject')
            college_grade = request.POST.get('college_grade')
            
            undergraduate_name = request.POST.get('undergraduate_name')
            undergraduate_city = request.POST.get('undergraduate_city')
            undergraduate_degree = request.POST.get('undergraduate_degree')
            undergraduate_major_subject = request.POST.get('undergraduate_major_subject')
            undergraduate_graduation_year = request.POST.get('undergraduate_graduation_year')
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
            employee_tax_number = request.POST.get('employee_tax_number')
            
            profile_picture = request.FILES.get('profile_picture')
            resume = request.FILES.get('resume')
            educational_certificates = request.FILES.get('educational_certificates')
            professional_certifications = request.FILES.get('professional_certifications')
            offer_letter = request.FILES.get('offer_letter')
            identity_proof = request.FILES.get('identity_proof')
            utility_bills = request.FILES.get('utility_bills')
            
            work_experience = request.POST.get('work_experience')
            skills = request.POST.get('skills')
            languages = request.POST.get('languages')
            hobbies = request.POST.get('hobbies')
            linkedin_profile = request.POST.get('linkedin_profile')
            professional_references = request.POST.get('professional_references')
            
            
            depart = Department.objects.filter(name=department).first()
            user = User()
            user.username = email
            user.email = email
            user.phone = phone
            user.name = name
            user.designation = designation
            user.department = depart
            user.active_password = password
            user.shift_duration_hours = working_hours
            user.is_staff = True
            
            user.dob = dob
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
            user.master_city =master_city
            user.master_degree = master_degree
            user.master_grade = master_grade
            user.master_graduation_year = master_graduation_year
            user.master_major_subject = master_major_subject
            
            user.phd_name = phd_name
            user.phd_city  =phd_city
            user.phd_degree = phd_degree
            user.phd_dissertation = phd_dissertation
            user.phd_graduation_year =phd_graduation_year
            user.phd_major_subject =phd_major_subject
            user.phd_supervisor =phd_supervisor
            
            user.bank_name = bank_name
            user.basic_salary = basic_salary
            user.fuel_allowance = fuel_allowance
            user.other_allowance = other_allowance
            user.employee_tax_number = employee_tax_number
            
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
                messages.success(request,'Employee Account Has Been Created')
                return redirect('index')
            except Exception as e:
                messages.error(request,"Please enter unique username/email")
                return redirect('create-employee-account')
            
        return render(request,'create-employee-account.html',context)
    else:
        return redirect('index')
    
    
@login_required(login_url='login')
def employees(request):
    employees = User.objects.all()
    context = {
        'employees':employees
    }
    return render(request,'employees.html',context)


@login_required(login_url='login')
def employee_delete(request,id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request,'Record has been deleted')
    
    return redirect('employees')