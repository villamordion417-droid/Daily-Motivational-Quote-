# Daily Motivational Quote App - Setup Guide

## Overview
This is a Django app that sends daily motivational quotes to subscribed users via email.

## Features
✨ **Core Features:**
- Store and manage motivational quotes
- User subscription management
- Daily email delivery of motivational quotes
- Customizable preferred delivery time per user
- Admin interface for managing quotes
- Beautiful HTML email templates
- Unsubscribe functionality
- Quote tracking and analytics

## Installation Steps

### 1. Install Required Packages
```bash
pip install -r requirements.txt
```

### 2. Apply Migrations
```bash
python manage.py migrate
```

### 3. Create a Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 4. Add Initial Quotes
1. Go to Django Admin: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Click on "Quotes"
4. Click "Add Quote"
5. Fill in the quote details:
   - Text: The motivational quote
   - Author: Who said it
   - Category: Choose from options (Motivation, Success, Perseverance, etc.)
   - Is Active: Check to include in daily send
6. Click "Save"

### 5. Test the App

#### Run Development Server
```bash
python manage.py runserver
```

#### Test Endpoints
- **Subscribe Page**: `http://localhost:8000/quotes/subscribe/`
- **Subscription Status**: `http://localhost:8000/quotes/status/` (requires login)
- **Latest Quote API**: `http://localhost:8000/quotes/api/latest/`

#### Send Test Quote (Console Output)
```bash
python manage.py send_daily_quote --all
```

The `--all` flag sends to all subscribers regardless of preferred time.

## Email Configuration

### For Development (Default)
The app is configured to print emails to the console (no actual email sent).
You'll see email content in the terminal.

### For Production with Gmail
1. Update `mysite/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password, not Gmail password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

2. For Gmail, create an "App Password":
   - Enable 2-Factor Authentication in Google Account
   - Go to myaccount.google.com/apppasswords
   - Select Mail and Windows Computer
   - Use the generated 16-character password

### For Other Email Services
Configure SMTP settings accordingly in `settings.py`

## Scheduling Daily Sends

### Option 1: Using Django-Crontab
Install: `pip install django-crontab`

Add to `settings.py`:
```python
CRONJOBS = [
    ('0 8 * * *', 'motivational_quotes.crons.send_daily_quotes'),
]
```

Start cron: `python manage.py crontab add`

### Option 2: Using Celery + Beat (Recommended for Production)
Install: `pip install celery redis`

Configure in `settings.py` and `motivational_quotes/tasks.py`

### Option 3: External Task Scheduler
Use services like:
- AWS Lambda
- Heroku Scheduler
- GitHub Actions
- External cron service

Run the command daily:
```bash
python manage.py send_daily_quote
```

## URL Routes

```
/quotes/subscribe/          - Subscribe to daily quotes
/quotes/unsubscribe/        - Unsubscribe from quotes
/quotes/status/             - View subscription status (requires login)
/quotes/update-time/        - Update preferred delivery time
/quotes/api/latest/         - Get latest quote as JSON
/admin/                     - Django admin panel
```

## Admin Features

### Quotes Management
- Add, edit, delete quotes
- Filter by category and active status
- Search quotes by text or author
- Bulk update is_active status

### Subscriptions Management
- View all subscriptions
- Deactivate/reactivate subscriptions
- Update preferred delivery times
- Track subscription dates

### Sent Quotes Analytics
- View all sent quotes
- Track which users received what
- Mark as opened for engagement tracking

## Database Models

### Quote
- text: TextField
- author: CharField
- category: ChoiceField (Motivation, Success, Perseverance, Courage, Inspiration, Growth, Wisdom)
- is_active: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField

### Subscription
- user: OneToOneField (User)
- email: EmailField
- is_active: BooleanField
- preferred_time: TimeField
- subscribed_at: DateTimeField
- unsubscribed_at: DateTimeField

### SentQuote
- quote: ForeignKey (Quote)
- subscription: ForeignKey (Subscription)
- sent_at: DateTimeField
- opened: BooleanField

## Sample Quotes to Add
Here are some motivational quotes to get you started:

1. "The only way to do great work is to love what you do." - Steve Jobs
2. "Believe you can and you're halfway there." - Theodore Roosevelt
3. "Success is not final, failure is not fatal." - Winston Churchill
4. "Don't watch the clock; do what it does. Keep going." - Sam Levenson
5. "The future belongs to those who believe in the beauty of their dreams." - Eleanor Roosevelt
6. "It is during our darkest moments that we must focus to see the light." - Aristotle
7. "The only impossible journey is the one you never begin." - Tony Robbins
8. "Great things never come from comfort zones." - Unknown
9. "Dream bigger. Do bigger." - Robin Sharma
10. "Success is walking from failure to failure with no loss of enthusiasm." - Winston Churchill

## Troubleshooting

### Quotes not sending
1. Check if subscriptions exist: `Subscription.objects.filter(is_active=True).count()`
2. Check if quotes exist: `Quote.objects.filter(is_active=True).count()`
3. Verify email configuration in settings
4. Check server logs for errors

### Users not seeing subscription page
1. Ensure user is logged in
2. Check if LOGIN_URL is configured
3. Verify templates are in correct directories

### Email not sending
1. Check email backend in settings
2. For Gmail: Verify app password is correct
3. Check firewall/network settings
4. Verify email credentials
5. Check Django logs for SMTP errors

## File Structure
```
motivational_quotes/
├── __init__.py
├── admin.py              # Admin interface configuration
├── apps.py               # App configuration
├── models.py             # Database models
├── views.py              # View logic
├── urls.py               # URL routing
├── management/
│   └── commands/
│       └── send_daily_quote.py    # Command to send quotes
├── templates/
│   └── motivational_quotes/
│       ├── subscribe.html         # Subscribe page
│       ├── unsubscribe.html       # Unsubscribe page
│       ├── status.html            # Subscription status
│       └── email/
│           └── daily_quote.html   # Email template
└── migrations/          # Database migrations
```

## Next Steps

1. ✅ Run migrations: `python manage.py migrate`
2. ✅ Create superuser: `python manage.py createsuperuser`
3. ✅ Add quotes via admin panel
4. ✅ Test send_daily_quote command
5. ✅ Set up email configuration
6. ✅ Configure scheduler for daily sends
7. ✅ Deploy to production

## Support & Questions

For more information on Django:
- Django Documentation: https://docs.djangoproject.com/
- Django Email: https://docs.djangoproject.com/en/6.0/topics/email/
- Django Management Commands: https://docs.djangoproject.com/en/6.0/howto/custom-management-commands/

Enjoy motivating your users! 🚀
