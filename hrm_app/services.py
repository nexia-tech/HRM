import pyautogui
from datetime import datetime
import os,time,boto3
from django.conf import settings

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
    
    try:
        os.remove(full_file_path)
    except Exception as e:
        pass

