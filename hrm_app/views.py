from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from hrm_app.models import AttendanceModel, EmployeeBreakRecords, ApplicantDetails, SystemAttendanceModel, ThumbAttendnace
from django.utils import timezone
from rest_framework.views import APIView
from datetime import timedelta, datetime
from rest_framework.response import Response
from math import floor
from django.contrib.auth.decorators import login_required
import pytz
from users.models import User, Department
from rest_framework import status
import threading
import time
import requests
from pynput import mouse, keyboard
from django.conf import settings
# from playsound import playsound
from hrm_app.services import take_screenshot
import random
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib import messages
from users.services import generate_password


BASE_URL = settings.BASE_URL


@login_required(login_url='login')
def my_attendance(request):
    user = request.user
    # attendances = AttendanceModel.objects.filter(employee=user)
    attendances = SystemAttendanceModel.objects.filter(
        employee=user).order_by('-shift_date').order_by('-shift_start_time')

    try:
        for attendance in attendances:
            attendance.remaining_hours = str(
                attendance.remaining_hours).split(".")[0]
    except Exception as e:
        print(e)
    context = {
        'attendances': attendances
    }

    return render(request, 'attendance-report.html', context)


@login_required(login_url='login')
def break_time_stamp(request, id):
    attendance = AttendanceModel.objects.get(id=id)
    context = {
        'attendance': attendance
    }

    return render(request, 'break-time-stamp.html', context)


@login_required(login_url='login')
def employees_report(request, id):
    # Fetch system attendance records
    system_attendances = SystemAttendanceModel.objects.all()
    thumb_attendances = ThumbAttendnace.objects.all()

    # Combine both attendances into a dictionary to display together
    combined_attendance = []
    for system in system_attendances:
        # Find matching thumb record by date
        thumb = thumb_attendances.filter(
            employee=system.employee, date=system.shift_date).first()
        system.remaining_hours = str(system.remaining_hours).split(".")[0]

        combined_attendance.append({
            'employee': system.employee,
            'shift_date': system.shift_date,
            'shift_start_time': system.shift_start_time,
            'time_out_time': system.time_out_time,
            'remaining_hours': system.remaining_hours,
            'is_present': system.is_present,
            'clock_in': thumb.clock_in if thumb else None,
            'clock_out': thumb.clock_out if thumb else None,
        })

    context = {
        'attendances': combined_attendance
    }
    return render(request, 'employees-report.html', context)


class UpdateTimeRecords(APIView):

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        user = User.objects.get(email=email)
        current_date = timezone.now().date()
        attendance_obj = AttendanceModel.objects.filter(
            employee__email=email, shift_date=current_date, is_time_out_marked=False).first()

        if not attendance_obj:
            return Response({'message': "Attendance not found", "status": False}, status=404)

        exist_record = EmployeeBreakRecords.objects.filter(
            employee=user, record_date=current_date, is_break_end=False).first()
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
            return Response({"message": "Your Shift has been ended"})

        # Split the string into hours, minutes, and seconds
        hours, minutes, seconds = map(int, remaining_hours_str.split(':'))

        # Create a timedelta object representing the duration
        time_duration = timedelta(
            hours=hours, minutes=minutes, seconds=seconds)

        # Convert timedelta to total milliseconds
        remaining_time_in_miliseconds = time_duration.total_seconds() * 1000

        remaining_time_in_miliseconds -= 1000

        hours = floor(remaining_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((remaining_time_in_miliseconds %
                        (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((remaining_time_in_miliseconds % (1000 * 60)) / 1000)

        remaining_time = timedelta(
            hours=hours, minutes=minutes, seconds=seconds)

        working_time_in_miliseconds = (
            attendance_obj.working_hours.total_seconds() * 1000)
        working_time_in_miliseconds += 1000

        hours = floor(working_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((working_time_in_miliseconds %
                        (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((working_time_in_miliseconds % (1000 * 60)) / 1000)

        working_hours = timedelta(
            hours=hours, minutes=minutes, seconds=seconds)

        # Update the attendance object with new calculations
        attendance_obj.working_hours = working_hours
        attendance_obj.remaining_hours = remaining_time
        attendance_obj.total_hours_completed = attendance_obj.working_hours + \
            attendance_obj.break_hours
        attendance_obj.save()

        # Return remaining time to frontend
        return Response({'meesage': "Updated", "remaining_hours": str(remaining_time), "status": True})


def playMusic():
    # for playing note.mp3 file
    playsound('break-tone.mp3')


class BreakTimeCalculate(APIView):

    def post(self, request):

        # threading.Thread(target=playMusic()).start()

        email = request.data.get('email')
        break_type = request.data.get('break_type', 'System Generated')
        comments = request.data.get('comments', None)

        if not email:
            return Response({'error': 'Email is required'}, status=400)

        current_date = timezone.now().date()
        attendance_obj = AttendanceModel.objects.filter(
            employee__email=email, shift_date=current_date, is_time_out_marked=False).first()

        if not attendance_obj:
            return Response({'message': "Attendance not found"}, status=404)

        user = User.objects.get(email=email)

        # add break records time stamp
        exist_record = EmployeeBreakRecords.objects.filter(
            employee=user, record_date=current_date, break_type=break_type, is_break_end=False).first()
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
            break_start_time_obj = datetime.strptime(
                karachi_time_str, "%H:%M:%S")

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
            return Response({"message": "Your Shift has been ended"})

        # Split the string into hours, minutes, and seconds
        hours, minutes, seconds = map(int, remaining_hours_str.split(':'))

        # Create a timedelta object representing the duration
        time_duration = timedelta(
            hours=hours, minutes=minutes, seconds=seconds)

        # Convert timedelta to total milliseconds
        remaining_time_in_miliseconds = time_duration.total_seconds() * 1000

        remaining_time_in_miliseconds -= 1000

        hours = floor(remaining_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((remaining_time_in_miliseconds %
                        (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((remaining_time_in_miliseconds % (1000 * 60)) / 1000)

        remaining_time = timedelta(
            hours=hours, minutes=minutes, seconds=seconds)

        break_time_in_miliseconds = (
            attendance_obj.break_hours.total_seconds() * 1000)
        break_time_in_miliseconds += 1000

        hours = floor(break_time_in_miliseconds / (1000 * 60 * 60))
        minutes = floor((break_time_in_miliseconds %
                        (1000 * 60 * 60)) / (1000 * 60))
        seconds = floor((break_time_in_miliseconds % (1000 * 60)) / 1000)

        breaking_hours = timedelta(
            hours=hours, minutes=minutes, seconds=seconds)
        # Update the attendance object with new calculations
        attendance_obj.break_hours = breaking_hours
        attendance_obj.remaining_hours = remaining_time
        attendance_obj.total_hours_completed = attendance_obj.working_hours + \
            attendance_obj.break_hours
        if exist_record is not None:
            attendance_obj.break_time_stamp.add(exist_record)
        attendance_obj.save()

        # Return remaining time to frontend
        return Response({'meesage': "Break Time Updated", "remaining_hours": str(remaining_time)})


class TimeOut(APIView):

    def post(self, request):
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
        attendance_obj = AttendanceModel.objects.filter(
            employee__email=email, shift_date=current_date, is_time_out_marked=False).first()
        if attendance_obj is None:
            return Response({"message": "No Attendance Found", "status": False})

        attendance_obj.is_time_out_marked = True
        attendance_obj.time_out_time = time_out_time
        attendance_obj.save()

        return Response({"message": "Time Out Successfully", "status": True})


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


def schedule_screenshot(email):
    global stop_thread
    while not stop_thread:
        interval = random.randint(1, 10) * 60  # interval in seconds
        print(
            f"Waiting for {interval / 60} minutes before taking the next screenshot.")
        time.sleep(interval)
        take_screenshot(email)


# Idle check function
def check_idle(email):
    global idle_time, stop_thread
    # Start the screenshot scheduler thread
    # screenshot_thread = threading.Thread(target=schedule_screenshot, args=(email,))
    # screenshot_thread.start()

    while not stop_thread:

        data = {
            "email": email
        }
        time.sleep(1)
        idle_time += 1
        if idle_time >= idle_threshold:

            r = requests.post(
                f"http://ec2-34-226-12-37.compute-1.amazonaws.com/hrm/break-time-record/", json=data)
            print(r.status_code)

        else:
            r2 = requests.post(
                f"http://ec2-34-226-12-37.compute-1.amazonaws.com/hrm/update-time-record/", json=data)
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
            try:
                keyboard_listener.start()
            except Exception as e:
                pass
            idle_check_thread = threading.Thread(
                target=check_idle, args=(email,))
            idle_check_thread.start()

            return Response({'status': 'Thread started', "success": True}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Thread already running', "success": False}, status=status.HTTP_200_OK)

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


@method_decorator(csrf_exempt, name='dispatch')
class ApplicantDetailsAPI(APIView):
    def post(self, request, *args, **kwargs):
        # try:
        # Get the data from request
        data = request.data
        print(data)

        # Get files if present (profile picture and resume)
        upload_profile = request.FILES.get('profile_picture')
        resume = request.FILES.get('resume')

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

        intermediate_details['institute'] = data.get(
            'intermediate_institute', None)
        intermediate_details['degree'] = data.get(
            'intermediate_degree', None)
        intermediate_details['percentage'] = data.get(
            'intermediate_grade', None)
        intermediate_details['year_passing'] = data.get(
            'intermediate_passing_year', None)

        bachelors_details['institute'] = data.get(
            'bachelors_institute', None)
        bachelors_details['degree'] = data.get('bachelors_degree', None)
        bachelors_details['percentage'] = data.get('bachelors_grade', None)
        bachelors_details['year_passing'] = data.get(
            'bachelors_year_passing', None)

        masters_details['institute'] = data.get('masters_institute', None)
        masters_details['degree'] = data.get('masters_degree', None)
        masters_details['percentage'] = data.get('masters_grade', None)
        masters_details['year_passing'] = data.get(
            'masters_year_passing', None)

        phd_details['institute'] = data.get(
            'phsign-up-report/d_institute', None)
        phd_details['degree'] = data.get('phd_degree', None)
        phd_details['percentage'] = data.get('phd_grade', None)
        phd_details['year_passing'] = data.get('phd_year_passing', None)

        diploma_details['institute'] = data.get('diploma_institute', None)
        diploma_details['degree'] = data.get('diploma_degree', None)
        diploma_details['percentage'] = data.get('diploma_grade', None)
        diploma_details['year_passing'] = data.get(
            'diploma_year_passing', None)

        job_experience_1_name_of_company = data.get(
            'job1_company_name', None)
        job_experience_1_department = data.get('job1_department', None)
        job_experience_1_position = data.get('job1_designation', None)
        job_experience_1_joinig_date = data.get('job1_joining_date', None)
        job_experience_1_end_date = data.get('job1_end_date', None)
        job_experience_1_salary = data.get('job1_salary', None)
        job_experience_1_experience_letter = data.get(
            'job1_experience_letter', None)
        job_experience_1_reason_for_leaving_job = data.get(
            'job1_reason', None)

        job_experience_2_name_of_company = data.get(
            'job2_company_name', None)
        job_experience_2_department = data.get('job2_department', None)
        job_experience_2_position = data.get('job2_designation', None)
        job_experience_2_joinig_date = data.get('job2_joining_date', None)
        job_experience_2_end_date = data.get('job2_end_date', None)
        job_experience_2_salary = data.get('job2_salary', None)
        job_experience_2_experience_letter = data.get(
            'job2_experience_letter', None)
        job_experience_2_reason_for_leaving_job = data.get(
            'job2_reason', None)

        job_experience_3_name_of_company = data.get(
            'job3_company_name', None)
        job_experience_3_department = data.get('job3_department', None)
        job_experience_3_position = data.get('job3_designation', None)
        job_experience_3_joinig_date = data.get('job3_joining_date', None)
        job_experience_3_end_date = data.get('job3_end_date', None)
        job_experience_3_salary = data.get('job3_salary', None)
        job_experience_3_experience_letter = data.get(
            'job3_experience_letter', None)
        job_experience_3_reason_for_leaving_job = data.get(
            'job3_reason', None)

        job_experience = [{
            "company_name": job_experience_1_name_of_company, "position": job_experience_1_position, "department": job_experience_1_department, "joining_date": job_experience_1_joinig_date, "salary": job_experience_1_salary, "experience_letter": job_experience_1_experience_letter, "reason_leaving": job_experience_1_reason_for_leaving_job,"job_experience_1_end_date":job_experience_1_end_date
        }, {
            "company_name": job_experience_2_name_of_company, "position": job_experience_2_position, "department": job_experience_2_department, "joining_date": job_experience_2_joinig_date, "salary": job_experience_2_salary, "experience_letter": job_experience_2_experience_letter, "reason_leaving": job_experience_2_reason_for_leaving_job,"job_experience_2_end_date":job_experience_2_end_date
        }, {
            "company_name": job_experience_3_name_of_company, "position": job_experience_3_position, "department": job_experience_3_department, "joining_date": job_experience_3_joinig_date, "salary": job_experience_3_salary, "experience_letter": job_experience_3_experience_letter, "reason_leaving": job_experience_3_reason_for_leaving_job,"job_experience_3_end_date":job_experience_3_end_date
        }]

        # Extract the fields from the POST data
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        name = first_name + last_name
        position_applied_for = data.get('position_applied_for', None)
        father_name = data.get('father_name', None)
        email_address = data.get('email_address', None)
        cnic = data.get('cnic', None)
        date_of_birth = data.get('date_of_birth', None)
        other_mobile_number = data.get('other_mobile_number', None)
        marital_status = data.get('marital_status', None)
        expected_salary = data.get('expected_salary', None)
        address = data.get('address', None)
        contact_number = data.get('contact_number', None)
        emergency_contact_number = data.get(
            'emergency_contact_number', None)
        when_join_us = data.get('when_join_us', None)
        shift_availablity = data.get('shift_availablity', None)
        matric_details = matric_details
        intermediate_details = intermediate_details
        bachelors_details = bachelors_details
        masters_details = masters_details
        phd_details = phd_details
        diploma_details = diploma_details
        job_experience = job_experience
        # Assuming it's a checkbox or boolean field
        declaration = data.get('declaration', False)

        exist = ApplicantDetails.objects.filter(
            email_address=email_address).first()

        if exist:
            return Response({
                'error': "Email already exisit",
                'message': 'Email already exisit'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create an ApplicantDetails object

        applicant = ApplicantDetails.objects.create(
            name=name,
            position_applied_for=position_applied_for,
            father_name=father_name,
            email_address=email_address,
            cnic=cnic,
            marital_status=marital_status,
            expected_salary=expected_salary,
            address=address,
            contact_number=contact_number,
            emergeny_contact_number=emergency_contact_number,
            when_join_us=when_join_us,
            shift_availablity=shift_availablity,
            matric_details=matric_details,
            intermediate_details=intermediate_details,
            bachelors_details=bachelors_details,
            masters_details=masters_details,
            phd_details=phd_details,
            diploma_details=diploma_details,
            job_experience=job_experience,
            upload_profile=upload_profile,
            resume=resume,
            other_mobile_number=other_mobile_number,
            declaration=declaration
        )

        try:
            applicant.date_of_birth = date_of_birth
            applicant.save()
        except Exception as e:
            print(e)

        return redirect('https://nexiatech.org/thankyou')
        # Return a success response
        return Response({
            'message': 'Applicant created successfully!',
            'applicant_id': applicant.id
        }, status=status.HTTP_201_CREATED)

        # except Exception as e:
        print(e)
        return Response({
            'error': str(e),
            'message': 'Failed to create applicant'
        }, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def applicant_detail_form_function(request):
    if request.method == 'POST':
        # try:
        # Get the data from request
        data = request.POST
        print(data)

        # Get files if present (profile picture and resume)
        upload_profile = request.FILES.get('profile_picture')
        resume = request.FILES.get('resume')

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

        intermediate_details['institute'] = data.get(
            'intermediate_institute', None)
        intermediate_details['degree'] = data.get(
            'intermediate_degree', None)
        intermediate_details['percentage'] = data.get(
            'intermediate_grade', None)
        intermediate_details['year_passing'] = data.get(
            'intermediate_passing_year', None)

        bachelors_details['institute'] = data.get(
            'bachelors_institute', None)
        bachelors_details['degree'] = data.get('bachelors_degree', None)
        bachelors_details['percentage'] = data.get('bachelors_grade', None)
        bachelors_details['year_passing'] = data.get(
            'bachelors_year_passing', None)

        masters_details['institute'] = data.get('masters_institute', None)
        masters_details['degree'] = data.get('masters_degree', None)
        masters_details['percentage'] = data.get('masters_grade', None)
        masters_details['year_passing'] = data.get(
            'masters_year_passing', None)

        phd_details['institute'] = data.get(
            'phsign-up-report/d_institute', None)
        phd_details['degree'] = data.get('phd_degree', None)
        phd_details['percentage'] = data.get('phd_grade', None)
        phd_details['year_passing'] = data.get('phd_year_passing', None)

        diploma_details['institute'] = data.get('diploma_institute', None)
        diploma_details['degree'] = data.get('diploma_degree', None)
        diploma_details['percentage'] = data.get('diploma_grade', None)
        diploma_details['year_passing'] = data.get(
            'diploma_year_passing', None)

        job_experience_1_name_of_company = data.get(
            'job1_company_name', None)
        job_experience_1_department = data.get('job1_department', None)
        job_experience_1_position = data.get('job1_designation', None)
        job_experience_1_joinig_date = data.get('job1_joining_date', None)
        job_experience_1_end_date = data.get('job1_end_date', None)
        job_experience_1_salary = data.get('job1_salary', None)
        job_experience_1_experience_letter = data.get(
            'job1_experience_letter', None)
        job_experience_1_reason_for_leaving_job = data.get(
            'job1_reason', None)

        job_experience_2_name_of_company = data.get(
            'job2_company_name', None)
        job_experience_2_department = data.get('job2_department', None)
        job_experience_2_position = data.get('job2_designation', None)
        job_experience_2_joinig_date = data.get('job2_joining_date', None)
        job_experience_2_end_date = data.get('job2_end_date', None)
        job_experience_2_salary = data.get('job2_salary', None)
        job_experience_2_experience_letter = data.get(
            'job2_experience_letter', None)
        job_experience_2_reason_for_leaving_job = data.get(
            'job2_reason', None)

        job_experience_3_name_of_company = data.get(
            'job3_company_name', None)
        job_experience_3_department = data.get('job3_department', None)
        job_experience_3_position = data.get('job3_designation', None)
        job_experience_3_joinig_date = data.get('job3_joining_date', None)
        job_experience_3_end_date = data.get('job3_end_date', None)
        job_experience_3_salary = data.get('job3_salary', None)
        job_experience_3_experience_letter = data.get(
            'job3_experience_letter', None)
        job_experience_3_reason_for_leaving_job = data.get(
            'job3_reason', None)

        job_experience = [{
            "company_name": job_experience_1_name_of_company, "position": job_experience_1_position, "department": job_experience_1_department, "joining_date": job_experience_1_joinig_date, "salary": job_experience_1_salary, "experience_letter": job_experience_1_experience_letter, "reason_leaving": job_experience_1_reason_for_leaving_job,"end_date":job_experience_1_end_date
        }, {
            "company_name": job_experience_2_name_of_company, "position": job_experience_2_position, "department": job_experience_2_department, "joining_date": job_experience_2_joinig_date, "salary": job_experience_2_salary, "experience_letter": job_experience_2_experience_letter, "reason_leaving": job_experience_2_reason_for_leaving_job,"end_date":job_experience_2_end_date
        }, {
            "company_name": job_experience_3_name_of_company, "position": job_experience_3_position, "department": job_experience_3_department, "joining_date": job_experience_3_joinig_date, "salary": job_experience_3_salary, "experience_letter": job_experience_3_experience_letter, "reason_leaving": job_experience_3_reason_for_leaving_job,"end_date":job_experience_3_end_date
        }]

        # Extract the fields from the POST data
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        name = first_name + " "+ last_name
        position_applied_for = data.get('position_applied_for', None)
        father_name = data.get('father_name', None)
        email_address = data.get('email_address', None)
        cnic = data.get('cnic', None)
        date_of_birth = data.get('date_of_birth', None)
        other_mobile_number = data.get('other_mobile_number', None)
        marital_status = data.get('marital_status', None)
        expected_salary = data.get('expected_salary', None)
        address = data.get('address', None)
        contact_number = data.get('contact_number', None)
        emergency_contact_number = data.get(
            'emergency_contact_number', None)
        when_join_us = data.get('when_join_us', None)
        emergency_contact_relation = data.get('emergency_contact_relation', None)
        gender = data.get('gender',None)
        shift_availablity = data.get('shift_availablity', None)
        matric_details = matric_details
        intermediate_details = intermediate_details
        bachelors_details = bachelors_details
        masters_details = masters_details
        phd_details = phd_details
        diploma_details = diploma_details
        job_experience = job_experience
        # Assuming it's a checkbox or boolean field
        declaration = data.get('declaration', False)

        exist = ApplicantDetails.objects.filter(
            email_address=email_address).first()

        if exist:
            return Response({
                'error': "Email already exisit",
                'message': 'Email already exisit'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create an ApplicantDetails object

        applicant = ApplicantDetails.objects.create(
            name=name,
            position_applied_for=position_applied_for,
            father_name=father_name,
            email_address=email_address,
            cnic=cnic,
            marital_status=marital_status,
            expected_salary=expected_salary,
            address=address,
            gender=gender,
            contact_number=contact_number,
            emergeny_contact_number=emergency_contact_number,
            when_join_us=when_join_us,
            emergency_contact_relation=emergency_contact_relation,
            shift_availablity=shift_availablity,
            matric_details=matric_details,
            intermediate_details=intermediate_details,
            bachelors_details=bachelors_details,
            masters_details=masters_details,
            phd_details=phd_details,
            diploma_details=diploma_details,
            job_experience=job_experience,
            upload_profile=upload_profile,
            resume=resume,
            other_mobile_number=other_mobile_number,
            declaration=declaration
        )

        try:
            applicant.date_of_birth = date_of_birth
            applicant.save()
        except Exception as e:
            print(e)

        return redirect('https://nexiatech.org/thankyou')
        # Return a success response
        return Response({
            'message': 'Applicant created successfully!',
            'applicant_id': applicant.id
        }, status=status.HTTP_201_CREATED)

        # except Exception as e:
        print(e)
        return Response({
            'error': str(e),
            'message': 'Failed to create applicant'
        }, status=status.HTTP_400_BAD_REQUEST)

class ShiftStartTime(APIView):
    def post(self, request):
        email = request.data['email']
        employee = User.objects.filter(email=email).first()

        # Get the current time in UTC
        utc_now = datetime.utcnow()

        # Specify the timezone you want to convert to
        tz = pytz.timezone('Asia/Karachi')

        # Convert UTC time to the specified timezone
        karachi_time = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)

        # Format the time as HH:MM:SS string
        karachi_time_str = karachi_time.strftime("%H:%M:%S")

        current_date = timezone.now().date()

        attendance = SystemAttendanceModel.objects.filter(
            employee=employee, shift_date=current_date, is_time_out_marked=False, is_present=True).last()

        if attendance is None:
            attendance = SystemAttendanceModel()
            attendance.shift_date = current_date
            attendance.employee = employee
            attendance.shift_start_time = karachi_time_str
            attendance.is_present = True
            attendance.save()

        return Response({"success": True, "message": "Shift Start Attendance Marked", "start_time": attendance.shift_start_time})


class ShiftEndTime(APIView):
    def post(self, request):
        email = request.data['email']
        employee = User.objects.filter(email=email).first()
        utc_now = datetime.utcnow()

        # Specify the timezone you want to convert to
        tz = pytz.timezone('Asia/Karachi')

        # Convert UTC time to the specified timezone
        karachi_time = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)

        # Format the time as HH:MM:SS string
        karachi_time_str = karachi_time.strftime("%H:%M:%S")

        # Get current date
        current_date = timezone.now().date()

        # Find the attendance record
        attendance = SystemAttendanceModel.objects.filter(
            employee=employee, shift_date=current_date, is_time_out_marked=False, is_present=True).last()

        if attendance:
            # Convert attendance.shift_start_time to datetime object
            shift_start_time = karachi_time.replace(
                hour=attendance.shift_start_time.hour, minute=attendance.shift_start_time.minute, second=attendance.shift_start_time.second, microsecond=0)


            # If shift_start_time is after karachi_time, adjust the date
            if shift_start_time > karachi_time:
                shift_start_time -= timedelta(days=1)
                
                
           # Calculate time passed since shift start
            time_passed = karachi_time - shift_start_time

            # Subtract time_passed from remaining_hours
            attendance.remaining_hours = max(
                timedelta(0), attendance.remaining_hours - time_passed
            )

            # Mark shift as ended
            attendance.time_out_time = karachi_time_str
            attendance.is_time_out_marked = True
            attendance.save()

        return Response({"success": True, "message": "Shift End Attendance Marked", "end_time": attendance.time_out_time})


def thumbAttendance(request, id):
    attendances = ThumbAttendnace.objects.filter(employee__id=id)
    user = User.objects.get(id=id)
    params = {'attendances': attendances}
    return render(request, 'thumb-attedance.html', params)

def systemAttendance(request, id):
    attendances = SystemAttendanceModel.objects.filter(employee__id=id)
    user = User.objects.get(id=id)
    params = {'attendances': attendances}
    return render(request, 'attendance-report.html', params)


def applicants(request):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    applicant_records = ApplicantDetails.objects.filter(is_employee=False).exclude(status='Junk')
    departments = Department.objects.all()
    params = {
        'applicant_records': applicant_records,
        'departments':departments
    }
    return render(request, 'applicant-records.html', params)


def applicant_detail(request, id):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    applicant_record = ApplicantDetails.objects.get(id=id)

    # Check if any field is None or an empty string
    any_field_empty = any(
        getattr(applicant_record, field.name) in [None, '']  # Check for None or empty string
        for field in applicant_record._meta.fields
    )
    print(any_field_empty)
    
  
    params = {
        'any_field_empty': any_field_empty,
        'applicant_record': applicant_record
    }
    return render(request, 'applicant-profile.html', params)


def get_csrf_token(request):
    # Return the CSRF token as a JSON response
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


class Mark_as_Employee(APIView):
    
    def post(self,request,id):
        record = ApplicantDetails.objects.get(id=id)
        user = User.objects.filter(email=record.email_address).first()
        data = request.data
        email_address = data.get('email_address')
        shift_duration = data.get('shift_duration')
        profile_picture = request.FILES.get('profile_picture')
        designation = data.get('designation')
        department = data.get('department')
        doj = data.get('doj')
        shift_timing = data.get('shift_timing')
        shift_end_timing = data.get('shift_end_timing')
        
        working_status = data.get('working_status')
        supervisor_name = data.get('supervisor_name')
        references = data.get('references')
        basic_salary = data.get('basic_salary')
        fuel_alloance = data.get('fuel_alloance')
        other_allowance = data.get('other_allowance')
        bank_name = data.get('bank_name')
        education_certification = request.FILES.get('education_certification')
        professional_certification = request.FILES.get('professional_certification')
        offer_letter = request.FILES.get('offer_letter')
        identity_proof = request.FILES.get('identity_proof')
        utility_bills = request.FILES.get('utility_bills')
        experience_certificate = request.FILES.get('experience_certificate')
        language = data.get('language')
        skills = data.get('skills')
        hobbies = data.get('hobbies')
        linkedin_link = data.get('linkedin_link')
        job_description = data.get('job_description')
        
        if not user:
            last_employee = User.objects.all().order_by('-employee_id').first()
            employee_id = int(last_employee.employee_id.split("-")[1]) + 1
            if employee_id < 100:
                employee_id = f"NX-0{str(employee_id)}"
            else:
                employee_id = f"NX-{str(employee_id)}"
            
            department = Department.objects.filter(name=department).first()
            user_obj = User()
            user_obj.name = record.name
            user_obj.username = record.email_address
            user_obj.email = record.email_address
            user_obj.cnic = record.cnic
            user_obj.address = record.address
            user_obj.doj = datetime.now().date()
            user_obj.resume  = record.resume
            user_obj.profile_picture = record.upload_profile
            user_obj.employee_id = employee_id
            password = generate_password()
            user_obj.set_password(password)
            user_obj.active_password = password
            user_obj.emergency_contact_name = record.emergency_contact_relation
            user_obj.phone = record.contact_number
            user_obj.martial_status = record.marital_status
            user_obj.dob = record.date_of_birth
            user_obj.company_email = email_address
            user_obj.shift_duration_hours = shift_duration
            user_obj.profile_picture = profile_picture
            user_obj.department = department
            user_obj.designation = designation
            user_obj.doj = doj
            user_obj.shift_timings = shift_timing
            user_obj.shift_end_timing=shift_end_timing
            user_obj.working_status = working_status
            user_obj.supervisor_name = supervisor_name
            user_obj.professional_references = references
            user_obj.basic_salary = basic_salary
            user_obj.fuel_allowance = fuel_alloance
            user_obj.other_allowance = other_allowance
            user_obj.bank_name = bank_name
            user_obj.educational_certificates = education_certification
            user_obj.professional_certifications = professional_certification
            user_obj.offer_letter = offer_letter
            user_obj.identity_proof = identity_proof
            user_obj.utility_bills = utility_bills
            user_obj.experience_certificate = experience_certificate
            user_obj.languages = language
            user_obj.skills = skills
            user_obj.hobbies = hobbies
            user_obj.linkedin_profile = linkedin_link
            user_obj.job_description = job_description
            user_obj.matric_details = record.matric_details 
            user_obj.intermediate_details = record.intermediate_details 
            user_obj.bachelors_details = record.bachelors_details 
            user_obj.masters_details = record.masters_details 
            user_obj.phd_details = record.phd_details 
            user_obj.diploma_details = record.diploma_details 
            user_obj.job_experience = record.job_experience 
            try:
                record.is_employee = True
                record.status = "Hired"
                user_obj.save()
                record.save()
                return Response({"message":"Employee Marked Successfully!!","status":True},status=200)
            except Exception as e:
                print(str(e))
                return Response({"message":f'Something went wrong {str(e)}', "status":False},status=400)
            
        else:
            messages.error(request, 'Email already exist on the record')
            return Response({"message":f'Email already exist on the record',"status":False},status=400)


class Mark_as_follow(APIView):
    
    def post(self,request,id):
        record = ApplicantDetails.objects.get(id=id)
        user = User.objects.filter(email=record.email_address).first()
        follow_up_date = request.data.get('follow_up_date')
        remarks = request.data.get('remarks')
        if not user:
            record.follow_up_date = follow_up_date
            record.remarks = remarks
            record.status = 'Follow up'
            record.save()
            messages.success(request, 'Employee Status Updated')
        else:
            messages.error(request, 'Email already exist on the record')
        return redirect('applicants')

class Mark_as_Shortlisted(APIView):
     def post(self,request,id):
        record = ApplicantDetails.objects.get(id=id)
        user = User.objects.filter(email=record.email_address).first()
        shortlisted_date = request.data.get('shortlisted_date')
        remarks = request.data.get('remarks')
        if not user:
            record.shortlisted_date = shortlisted_date
            record.remarks = remarks
            record.status = "Shortlisted"
            record.save()
            messages.success(request, 'Employee Status Updated')
        else:
            messages.error(request, 'Email already exist on the record')
        return redirect('applicants')


class SetSchedule(APIView):
     def post(self,request,id):
        record = ApplicantDetails.objects.get(id=id)
        user = User.objects.filter(email=record.email_address).first()
        scheduled_date = request.data.get('scheduled_date')
        scheduled_time = request.data.get('scheduled_time')
        remarks = request.data.get('comments')
        if not user:
            record.scheduled_date = scheduled_date
            record.scheduled_time = scheduled_time
            record.remarks = remarks
            record.is_scheduled = True
            record.status = "Scheduled"
            record.save()
            messages.success(request, 'Employee Status Updated')
            return Response(status=200)
        else:
            messages.error(request, 'Email already exist on the record')
            return Response(status=500)
    
class SetJunks(APIView):
     def post(self,request,id):
        record = ApplicantDetails.objects.get(id=id)
        user = User.objects.filter(email=record.email_address).first()
        if not user:
            record.status = "Junk"
            record.save()
            messages.success(request, 'Employee Status Updated')
            return Response(status=200)
        else:
            messages.error(request, 'Email already exist on the record')
            return Response(status=500)
    
class Mark_as_Rejected(APIView):
    
    def post(self,request,id):
        record = ApplicantDetails.objects.get(id=id)
        user = User.objects.filter(email=record.email_address).first()
        rejected = request.data.get('rejected')
        if not user:
            record.rejected_reason = rejected
            record.is_rejected = True
            record.status = "Rejected"
            record.save()
            messages.success(request, 'Employee Status Updated')
        else:
            messages.error(request, 'Email already exist on the record')
        return redirect('applicants')


def show_schedules_records(request):
    if not request.user.is_superuser:
        messages.error(request,"You don't have permission")
        return redirect('index')
    records = ApplicantDetails.objects.filter(is_scheduled=True)
    params = {
        'records':records
    }
    
    return render(request,'scedules-records.html', params)