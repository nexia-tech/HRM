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

    
@login_required(login_url='login')
def index(request):
    user = request.user


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
    current_time_12hr = datetime_obj.strftime("%I:%M:%S")

    # Create timedelta object representing shift duration (8 hours in this example)
    shift_duration_timedelta = timedelta(hours=user.shift_duration_hours)
    
    
    
    current_date = timezone.now().date()
    attendance_obj= AttendanceModel.objects.filter(employee=user,shift_date=current_date).first()

    
    if attendance_obj is None:
        attendance_object = AttendanceModel()
        attendance_object.employee = user
        attendance_object.shift_date = current_date
        attendance_object.shift_time = current_time_12hr
        attendance_object.remaining_hours = shift_duration_timedelta
        attendance_object.save()
    
    
    context ={
        'user':user,
        'attendance_obj':attendance_obj
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
                current_time_12hr = datetime_obj.strftime("%I:%M:%S")
    
                # Create timedelta object representing shift duration (8 hours in this example)
                shift_duration_timedelta = timedelta(hours=user.shift_duration_hours)
                

                attendance_obj= AttendanceModel.objects.filter(employee=user,shift_date=current_date).first()

               
                if attendance_obj is None:
                    attendance_object = AttendanceModel()
                    attendance_object.employee = user
                    attendance_object.shift_date = current_date
                    attendance_object.shift_time = current_time_12hr
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
            username = request.POST.get('username')
            email = request.POST.get('email')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            bio = request.POST.get('bio')
            profile_picture = request.FILES.get('profile_picture')
            department = request.POST.get('department')
            designation = request.POST.get('designation')
            password = request.POST.get('password')
            working_hours = request.POST.get('working_hours')
            
            
            depart = Department.objects.filter(name=department).first()
            user = User()
            user.username = username
            user.email = email
            user.phone = phone
            user.name = name
            user.bio = bio
            user.profile_picture = profile_picture
            user.designation = designation
            user.department = depart
            user.active_password = password
            user.shift_duration_hours = working_hours
            user.is_staff = True
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