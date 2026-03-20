@echo off
REM Daily Motivational Quote App - Helper Script for Windows

echo.
echo ===== Daily Motivational Quote App =====
echo.
echo Available commands:
echo.
echo 1. setup          - Initial setup (migrations + sample data)
echo 2. run            - Run development server
echo 3. admin          - Create superuser
echo 4. send-test      - Send test quote to all subscribers
echo 5. send-scheduled - Send quote (for scheduled tasks)
echo 6. add-quote      - Add quotes via interactive CLI
echo 7. list-quotes    - List all quotes
echo 8. migrate        - Apply database migrations
echo.

if "%1"=="setup" (
    echo Running setup...
    python manage.py migrate
    python manage.py shell < populate_quotes.py
    echo ✓ Setup complete! Create admin: python manage.py createsuperuser
) else if "%1"=="run" (
    echo Starting development server...
    python manage.py runserver
) else if "%1"=="admin" (
    echo Creating superuser...
    python manage.py createsuperuser
) else if "%1"=="send-test" (
    echo Sending test quote to all subscribers...
    python manage.py send_daily_quote --all
) else if "%1"=="send-scheduled" (
    echo Sending scheduled quote...
    python manage.py send_daily_quote
) else if "%1"=="migrate" (
    echo Running migrations...
    python manage.py migrate
) else if "%1"=="list-quotes" (
    echo Listing all quotes...
    python manage.py shell < list_quotes.py
) else (
    echo Please provide a command: setup, run, admin, send-test, send-scheduled, migrate, or list-quotes
)
