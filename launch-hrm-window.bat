@ECHO off

REM Start the Django development server
START /B /MIN cmdow @ /HID & python manage.py runserver

REM Start the npm process
START /B /MIN cmdow @ /HID & npm run hrm
