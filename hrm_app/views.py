from django.shortcuts import render
from hrm_app.models import AttendanceModel
from django.utils import timezone
from rest_framework.views import APIView
from datetime import timedelta,datetime
from rest_framework.response import Response
from math import floor    
from django.contrib.auth.decorators import login_required
# Create your views here.


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
        
        # Split the string into hours, minutes, and seconds
        hours, minutes, seconds = map(int, remaining_hours_str.split(':'))

        # Create a timedelta object representing the duration
        time_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

        # Convert timedelta to total milliseconds
        remaining_time_in_miliseconds = time_duration.total_seconds() * 1000
        

        remaining_time_in_miliseconds -= 1000

        hours = floor(remaining_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((remaining_time_in_miliseconds % (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((remaining_time_in_miliseconds % (1000 * 60)) / 1000)
        
        remaining_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        working_time_in_miliseconds = (attendance_obj.working_hours.total_seconds() * 1000)
        working_time_in_miliseconds += 1000
       
        hours = floor(working_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((working_time_in_miliseconds % (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((working_time_in_miliseconds % (1000 * 60)) / 1000)
        
        working_hours = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
      
        # Update the attendance object with new calculations
        attendance_obj.working_hours = working_hours
        attendance_obj.remaining_hours = remaining_time
        attendance_obj.total_hours_completed = attendance_obj.working_hours + attendance_obj.break_hours
        attendance_obj.save()
        
        # Return remaining time to frontend
        return Response({'meesage': "Updated","remaining_hours":str(remaining_time)})
    
@login_required(login_url='login')
def my_attendance(request):
    user = request.user
    attendances = AttendanceModel.objects.filter(employee=user)
    context = {
        'attendances':attendances
    }
    
    return render(request,'attendance-report.html',context)


class BreakTimeCalculate(APIView):
    
    def post(self,request):
        email = request.data.get('email')
        
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        
        current_date = timezone.now().date()
        attendance_obj = AttendanceModel.objects.filter(employee__email=email, shift_date=current_date).first()
        
        if not attendance_obj:
            return Response({'message': "Attendance not found"}, status=404)
        
        remaining_hours_str = str(attendance_obj.remaining_hours)
        
        # Split the string into hours, minutes, and seconds
        hours, minutes, seconds = map(int, remaining_hours_str.split(':'))

        # Create a timedelta object representing the duration
        time_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

        # Convert timedelta to total milliseconds
        remaining_time_in_miliseconds = time_duration.total_seconds() * 1000
        

        remaining_time_in_miliseconds -= 1000

        hours = floor(remaining_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((remaining_time_in_miliseconds % (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((remaining_time_in_miliseconds % (1000 * 60)) / 1000)
        
        remaining_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        break_time_in_miliseconds = (attendance_obj.break_hours.total_seconds() * 1000)
        break_time_in_miliseconds += 1000
       
        hours = floor(break_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((break_time_in_miliseconds % (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((break_time_in_miliseconds % (1000 * 60)) / 1000)
        
        breaking_hours = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        
        # Update the attendance object with new calculations
        attendance_obj.break_hours = breaking_hours
        attendance_obj.remaining_hours = remaining_time
        attendance_obj.total_hours_completed = attendance_obj.working_hours + attendance_obj.break_hours
        attendance_obj.save()
        
        # Return remaining time to frontend
        return Response({'meesage': "Break Time Updated","remaining_hours":str(remaining_time)})
        