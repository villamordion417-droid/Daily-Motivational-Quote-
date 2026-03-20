#!/bin/bash
# Daily Motivational Quote App - Helper Script for Unix/Linux/Mac

echo ""
echo "===== Daily Motivational Quote App ====="
echo ""
echo "Available commands:"
echo ""
echo "1. setup          - Initial setup (migrations + sample data)"
echo "2. run            - Run development server"
echo "3. admin          - Create superuser"
echo "4. send-test      - Send test quote to all subscribers"
echo "5. send-scheduled - Send quote (for scheduled tasks)"
echo "6. migrate        - Apply database migrations"
echo ""

case "$1" in
  setup)
    echo "Running setup..."
    python manage.py migrate
    python manage.py shell < populate_quotes.py
    echo "✓ Setup complete! Create admin: python manage.py createsuperuser"
    ;;
  run)
    echo "Starting development server..."
    python manage.py runserver
    ;;
  admin)
    echo "Creating superuser..."
    python manage.py createsuperuser
    ;;
  send-test)
    echo "Sending test quote to all subscribers..."
    python manage.py send_daily_quote --all
    ;;
  send-scheduled)
    echo "Sending scheduled quote..."
    python manage.py send_daily_quote
    ;;
  migrate)
    echo "Running migrations..."
    python manage.py migrate
    ;;
  *)
    echo "Please provide a command: setup, run, admin, send-test, send-scheduled, or migrate"
    ;;
esac
