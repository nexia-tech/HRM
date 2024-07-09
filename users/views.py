from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from users.models import User
from django.contrib.auth.decorators import login_required
from hrm_app.models import AttendanceModel
from django.utils import timezone
from datetime import datetime
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

@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        user.phone = phone
        user.name = name
        user.save()
        messages.success(request,'Profile has been updated')
        return redirect('index')
    else:
        context = {
            'user':user
        }
        return render(request,'edit-profile.html',context)