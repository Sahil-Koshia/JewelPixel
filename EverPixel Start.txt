@echo off
REM Change directory to the location of the Flask app
cd /d %~dp0

REM Activate the virtual environment (if you have one)
REM Replace 'venv' with the name of your virtual environment directory
call venv\Scripts\activate

REM Set environment variables for Flask
set FLASK_APP=app.py
set FLASK_ENV=development

REM Start the Flask application
flask run --host=0.0.0.0 --port=5000

pause
