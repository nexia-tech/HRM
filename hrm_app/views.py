from django.shortcuts import render,HttpResponseRedirect,redirect
from django.urls import reverse
from hrm_app.models import AttendanceModel, EmployeeBreakRecords
from django.utils import timezone
from rest_framework.views import APIView
from datetime import timedelta,datetime
from rest_framework.response import Response
from math import floor    
from django.contrib.auth.decorators import login_required
import pytz
from users.models import User
from rest_framework import status
import threading
import time, requests
from pynput import mouse, keyboard
from django.conf import settings
# from playsound import playsound




BASE_URL = settings.BASE_URL



@login_required(login_url='login')
def my_attendance(request):
    user = request.user
    attendances = AttendanceModel.objects.filter(employee=user)
    context = {
        'attendances':attendances
    }
    
    return render(request,'attendance-report.html',context)

@login_required(login_url='login')
def break_time_stamp(request,id):
    attendance = AttendanceModel.objects.get(id=id)
    context = {
        'attendance':attendance
    }
    
    return render(request,'break-time-stamp.html',context)





class UpdateTimeRecords(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        
        user = User.objects.get(email=email)
        current_date = timezone.now().date()
        attendance_obj = AttendanceModel.objects.filter(employee__email=email, shift_date=current_date,is_time_out_marked=False).first()
        
        if not attendance_obj:
            return Response({'message': "Attendance not found","status":False}, status=404)
       
        exist_record = EmployeeBreakRecords.objects.filter(employee=user,record_date=current_date,is_break_end=False).first()
        # Get the current time in UTC
        utc_now = datetime.utcnow()

        # Specify the timezone you want to convert to
        tz = pytz.timezone('Asia/Karachi')

        # Convert UTC time to the specified timezone
        karachi_time = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)

        # Format the time as HH:MM:SS string
        karachi_time_str = karachi_time.strftime("%H:%M:%S")
        
            # Convert string to datetime object
        break_end_time_obj = datetime.strptime(karachi_time_str, "%H:%M:%S")
            
        if exist_record is not None:
           
            exist_record.end_time = break_end_time_obj
            exist_record.is_break_end = True
            exist_record.save()
  
        remaining_hours_str = str(attendance_obj.remaining_hours)
        
        time_out_time = datetime.strptime(karachi_time_str, "%H:%M:%S")
        
        if remaining_hours_str == "0:00:00":
            attendance_obj.time_out_time = time_out_time
            attendance_obj.is_time_out_marked = True
            attendance_obj.save()
            return Response({"message":"Your Shift has been ended"})
        
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
        return Response({'meesage': "Updated","remaining_hours":str(remaining_time),"status":True})
    
    
    
def playMusic():
     # for playing note.mp3 file
    playsound('break-tone.mp3')
    
class BreakTimeCalculate(APIView):
    
    def post(self,request):
        
        
        # threading.Thread(target=playMusic()).start()

       
        email = request.data.get('email')
        break_type = request.data.get('break_type','System Generated')
        comments = request.data.get('comments',None)
        
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        
        current_date = timezone.now().date()
        attendance_obj = AttendanceModel.objects.filter(employee__email=email, shift_date=current_date, is_time_out_marked=False).first()
        
        if not attendance_obj:
            return Response({'message': "Attendance not found"}, status=404)
        
        user = User.objects.get(email=email)
        
        # add break records time stamp
        exist_record = EmployeeBreakRecords.objects.filter(employee=user,record_date=current_date,break_type=break_type,is_break_end=False).first()
         # Get the current time in UTC
        utc_now = datetime.utcnow()

        # Specify the timezone you want to convert to
        tz = pytz.timezone('Asia/Karachi')

        # Convert UTC time to the specified timezone
        karachi_time = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)

        # Format the time as HH:MM:SS string in 24-hour format
        karachi_time_str = karachi_time.strftime("%H:%M:%S")

        if exist_record is None:
            exist_record = EmployeeBreakRecords()
            exist_record.employee = user
            
           
            # Convert string to datetime object (24-hour format)
            break_start_time_obj = datetime.strptime(karachi_time_str, "%H:%M:%S")
            
            
            exist_record.start_time = break_start_time_obj
            exist_record.break_comments = comments
            exist_record.break_type = break_type
            exist_record.record_date = current_date
            exist_record.save()
        
        
        remaining_hours_str = str(attendance_obj.remaining_hours)
        time_out_time = datetime.strptime(karachi_time_str, "%H:%M:%S")
        
        if remaining_hours_str == "0:00:00":
            attendance_obj.time_out_time = time_out_time
            attendance_obj.is_time_out_marked = True
            attendance_obj.save()
            return Response({"message":"Your Shift has been ended"})
        
       
        
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
        if exist_record is not None:
            attendance_obj.break_time_stamp.add(exist_record)
        attendance_obj.save()

        
        
        # Return remaining time to frontend
        return Response({'meesage': "Break Time Updated","remaining_hours":str(remaining_time)})
        
        
class TimeOut(APIView):
    
    def post(self,request):
        # Get the current time in UTC
        utc_now = datetime.utcnow()

        # Specify the timezone you want to convert to
        tz = pytz.timezone('Asia/Karachi')

        # Convert UTC time to the specified timezone
        karachi_time = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)

        # Format the time as HH:MM:SS string
        karachi_time_str = karachi_time.strftime("%H:%M:%S")
        
        # Convert string to datetime object
        time_out_time = datetime.strptime(karachi_time_str, "%H:%M:%S").time()
        
        
        email = request.data.get('email')
        
        
        current_date = timezone.now().date()
        attendance_obj = AttendanceModel.objects.filter(employee__email=email, shift_date=current_date,is_time_out_marked=False).first()
        if attendance_obj is None:
            return Response({"message":"No Attendance Found","status":False})

        attendance_obj.is_time_out_marked = True
        attendance_obj.time_out_time = time_out_time
        attendance_obj.save()
        
        
        return Response({"message":"Time Out Successfully","status":True})
    

# Global variables
stop_thread = False
idle_time = 0
idle_threshold = 180  # 60 seconds for demonstration
idle_check_thread = None
mouse_listener = None
keyboard_listener = None
result = None
# Create an event object
done_event = threading.Event()

def reset_idle_time():
    global idle_time
    idle_time = 0

def on_move(x, y):
    reset_idle_time()

def on_click(x, y, button, pressed):
    reset_idle_time()

def on_scroll(x, y, dx, dy):
    reset_idle_time()

def on_press(key):
    reset_idle_time()

def on_release(key):
    reset_idle_time()


# Idle check function
def check_idle(email):
    global idle_time, stop_thread
    while not stop_thread:
        data = {
            "email":email
        }
        time.sleep(1)
        idle_time += 1
        if idle_time >= idle_threshold:
        
            r = requests.post(f"http://ec2-34-226-12-37.compute-1.amazonaws.com/hrm/break-time-record/",json=data)
            print(r.status_code)
            
        else:
            r2 = requests.post(f"http://ec2-34-226-12-37.compute-1.amazonaws.com/hrm/update-time-record/",json=data)
            print(r2.status_code)

# API View for starting the thread
class StartThreadView(APIView):
    def post(self, request):
        email = request.data.get('email')
        global stop_thread, idle_check_thread, mouse_listener, keyboard_listener
        if idle_check_thread is None or not idle_check_thread.is_alive():
            stop_thread = False
            mouse_listener = mouse.Listener(
                on_move=on_move,
                on_click=on_click,
                on_scroll=on_scroll
            )
            keyboard_listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release
            )
            mouse_listener.start()
            keyboard_listener.start()
            idle_check_thread = threading.Thread(target=check_idle,args=(email,))
            idle_check_thread.start()
            
            return Response({'status': 'Thread started',"success":True}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Thread already running',"success":False}, status=status.HTTP_200_OK)

# API View for stopping the thread
class StopThreadView(APIView):
    def post(self, request):
        email = request.data.get('email')
        global stop_thread, idle_check_thread, mouse_listener, keyboard_listener
        if idle_check_thread is not None and idle_check_thread.is_alive():
        
            stop_thread = True
            idle_check_thread.join()
            idle_check_thread = None
            if mouse_listener is not None:
                mouse_listener.stop()
                mouse_listener = None
            if keyboard_listener is not None:
                keyboard_listener.stop()
                keyboard_listener = None
            return Response({'status': 'Thread stopped'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Thread is not running'}, status=status.HTTP_400_BAD_REQUEST)
