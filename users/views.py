from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from users.models import User
from django.contrib.auth.decorators import login_required
from hrm_app.models import AttendanceModel
from django.utils import timezone
from rest_framework.views import APIView
from datetime import timedelta,datetime
from rest_framework.response import Response
from math import floor    
    
@login_required(login_url='login')
def index(request):
    user = request.user

    current_time_str = timezone.now().time().strftime("%H:%M:%S")
    current_time = datetime.strptime(current_time_str, "%H:%M:%S").time()
    current_date = timezone.now().date()
    attendance_obj= AttendanceModel.objects.filter(employee=user,shift_date=current_date).first()


    if attendance_obj is None:
        attendance_object = AttendanceModel()
        attendance_object.employee = user
        attendance_object.shift_date = current_date
        attendance_object.shift_time = current_time
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
                current_time_str = timezone.now().time().strftime("%H:%M:%S")
                current_time = datetime.strptime(current_time_str, "%H:%M:%S").time()

                attendance_obj= AttendanceModel.objects.filter(employee=user,shift_date=current_date).first()


                if attendance_obj is None:
                    attendance_object = AttendanceModel()
                    attendance_object.employee = user
                    attendance_object.shift_date = current_date
                    attendance_object.shift_time = current_time
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


class UpdateTimeRecords(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        
        current_date = timezone.now().date()
        attendance_obj = AttendanceModel.objects.filter(employee__email=email, shift_date=current_date).first()
        
        if not attendance_obj:
            return Response({'message': "Attendance not found"}, status=404)
       
  
        remaining_hours_str = str(attendance_obj.remaining_hours)
        print(remaining_hours_str)        
        
                # Split the string into hours, minutes, and seconds
        hours, minutes, seconds = map(int, remaining_hours_str.split(':'))

        # Create a timedelta object representing the duration
        time_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        print(time_duration)

        # Convert timedelta to total milliseconds
        remaining_time_in_miliseconds = time_duration.total_seconds() * 1000
        
        print("remaining_time_in_miliseconds: ",remaining_time_in_miliseconds)

        remaining_time_in_miliseconds -= 1000

        hours = floor(remaining_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((remaining_time_in_miliseconds % (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((remaining_time_in_miliseconds % (1000 * 60)) / 1000)
        
        remaining_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        print(remaining_time)
        
        working_time_in_miliseconds = (attendance_obj.working_hours.total_seconds() * 1000)
        working_time_in_miliseconds += 1000
       
        hours = floor(working_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((working_time_in_miliseconds % (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((working_time_in_miliseconds % (1000 * 60)) / 1000)
        
        working_hours = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        print(working_hours)
        
      
        # Update the attendance object with new calculations
        attendance_obj.working_hours = working_hours
        attendance_obj.remaining_hours = remaining_time
        attendance_obj.total_hours_completed = attendance_obj.working_hours + attendance_obj.break_hours
        attendance_obj.save()
        
        # Return remaining time to frontend
        return Response({'meesage': "Updated"})