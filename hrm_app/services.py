import pyautogui
from datetime import datetime
import os,time,boto3, base64, requests
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
    date =str(datetime.now().strftime("%D")).replace("/",'-')
    directory_path = os.path.join('screenshots', month_year,email,date)
    # print(f"directory path: {directory_path}")
    # Create the directory if it doesn't exist
    
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
    directory_path = directory_path.replace("\\","/")
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
    print("Savedddd")
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
    


DEVICE_IP = settings.DEVICE_IP

USERNAME = settings.HIKVISION_USERNAME
PASSWORD = settings.HIKVISION_PASSWORD


def get_hikvision_machine_attendance():
    credentials = f"{USERNAME}:{PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://isgp-team.hikcentralconnect.com/hcc/hccattendance/report/v1/list"

    payload = {
        "page": 1,
        "pageSize": 100,
        "language": "en",
        "reportTypeId": 2,
        "columnIdList": [],
        "filterList": [
            {
                "columnName": "fullName",
                "operation": "LIKE",
                "value": ""
            },
            {
                "columnName": "personCode",
                "operation": "LIKE",
                "value": ""
            },
            {
                "columnName": "groupId",
                "operation": "IN",
                "value": ""
            },
            {
                "columnName": "date",
                "operation": "BETWEEN",
                "value": "2025-02-07T00:00:00+05:00,2025-02-07T23:59:59+05:00"
            }
        ]
    }
    headers = {
        "authority": "isgp-team.hikcentralconnect.com",
        "method": "POST",
        "path": "/hcc/hccattendance/report/v1/list",
        "scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,ru;q=0.8,ar;q=0.7",
        "content-length": "363",
        "content-type": "application/json",
        "cookie": "JSESSIONID=d891384c-930e-467c-96d0-4e9c64ec9d37",
        "origin": "https://isgp-team.hikcentralconnect.com",
        "priority": "u=1, i",
        "referer": "https://isgp-team.hikcentralconnect.com/team/index.html?lang=en&t=1738957122113&origin=https://isgp.hik-connect.com",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-gray-version": "20241114003"
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.text)

    return response.json()