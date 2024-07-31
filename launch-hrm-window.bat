@ECHO off

REM Start the Django development server
START /MIN python manage.py runserver

REM Start the npm process
START /MIN npm run hrm