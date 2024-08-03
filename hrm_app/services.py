import pyautogui
from datetime import datetime
import os,time,boto3
from django.conf import settings
from hrm_app.models import ScreenShotRecords
from users.models import User

aws_access_key_id = settings.AWS_ACCESS_KEY_ID
aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

aws_region='us-east-1'
s3_client = boto3.client('s3', region_name=aws_region,aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


def take_screenshot(email):
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    # Generate a filename with timestamp
    month_year = datetime.now().strftime("%B-%Y")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'screenshot_{email}_{timestamp}.png'
    directory_path = os.path.join('screenshots', month_year,email)
    # print(f"directory path: {directory_path}")
    # Create the directory if it doesn't exist
    try:
        os.makedirs(directory_path)
    except FileExistsError:
        pass
    
    
    # Define the full file path
    full_file_path = os.path.join(directory_path, filename)
    # Save the screenshot to a file
    screenshot.save(full_file_path)
    # Upload the file to S3
    s3_client.upload_file(full_file_path, 'nexia-hrm', full_file_path)
    # print("Savedddd")
    employee = User.objects.filter(email=email).first()
    
    date = datetime.now().date()
    
    s3_complete_link = f"https://nexia-hrm.s3.amazonaws.com/{full_file_path}"
    ScreenShotRecords.objects.create(
        employee=employee,
        date=date,
        s3_screen_shot_link=s3_complete_link
    )
    try:
        os.remove(full_file_path)
    except Exception as e:
        pass

