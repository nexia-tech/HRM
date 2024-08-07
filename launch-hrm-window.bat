@ECHO off

@REM REM Start the Django development server
START /B python manage.py runserver

@REM REM Start the npm process
START /B npm run hrm
