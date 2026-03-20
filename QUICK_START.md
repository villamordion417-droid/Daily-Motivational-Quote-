# Daily Motivational Quote App - Quick Reference Card

## 🎯 In 5 Minutes

```bash
cd mysite
python manage.py migrate
python manage.py createsuperuser
python manage.py shell < ../populate_quotes.py
python manage.py runserver
```

Then visit: **http://localhost:8000/admin/**

---

## 📋 Key Routes

| What | URL |
|------|-----|
| Admin Panel | http://localhost:8000/admin/ |
| Subscribe | http://localhost:8000/quotes/subscribe/ |
| My Subscriptions | http://localhost:8000/quotes/status/ |
| API Latest Quote | http://localhost:8000/quotes/api/latest/ |

---

## 🎮 Key Commands

```bash
# Setup
python manage.py migrate                 # Database
python manage.py createsuperuser         # Admin account

# Populate
python manage.py shell < populate_quotes.py

# Run
python manage.py runserver               # Start server

# Send test
python manage.py send_daily_quote --all  # Send to all now

# Tests
python manage.py test motivational_quotes
```

---

## 📧 Email Configuration

**Development (Default):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Emails print to console.

**Gmail Production:**
Update `mysite/settings.py`:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

Get app password: https://myaccount.google.com/apppasswords

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `mysite/settings.py` | Email & app config |
| `mysite/urls.py` | URL routing |
| `motivational_quotes/models.py` | Database models |
| `motivational_quotes/views.py` | View logic |
| `motivational_quotes/admin.py` | Admin interface |
| `motivational_quotes/management/commands/send_daily_quote.py` | Send command |
| `populate_quotes.py` | Sample data |
| `SETUP_GUIDE.md` | Detailed guide |
| `README.md` | Full documentation |

---

## 🔧 Admin Quick Tips

**Add Quote:**
1. Login to http://localhost:8000/admin/
2. Click "Quotes" → "Add Quote"
3. Fill in text, author, category
4. Check "Is active"
5. Save

**Send Test Quote:**
```bash
python manage.py send_daily_quote --all
```

**View Subscriptions:**
1. Go to admin
2. Click "Subscriptions"
3. See all users & their times

---

## 🧪 Testing

```bash
# Run all tests
python manage.py test motivational_quotes

# Run specific test
python manage.py test motivational_quotes.tests.QuoteModelTest

# With verbose output
python manage.py test motivational_quotes -v 2
```

---

## ⏰ Schedule Daily Send

**Windows Task Scheduler:**
1. Create task
2. Trigger: Daily, 8:00 AM
3. Action: `python.exe` 
4. Arguments: `"C:\path\manage.py" send_daily_quote`

**Linux Cron:**
```bash
0 8 * * * cd /path/mysite && python manage.py send_daily_quote
```

---

## 🐛 Quick Fixes

| Issue | Fix |
|-------|-----|
| App not found | `pip install -r requirements.txt` then restart |
| Emails not sending | Check EMAIL_BACKEND setting |
| Port 8000 busy | `python manage.py runserver 8001` |
| Database error | `rm db.sqlite3` then `python manage.py migrate` |
| Permission denied | Make sure you're in `mysite` directory |

---

## 💡 Database Models Summary

### Quote
- text, author, category, is_active
- Categories: motivation, success, perseverance, courage, inspiration, growth, wisdom

### Subscription
- user, email, is_active, preferred_time (e.g., 08:00)

### SentQuote
- quote, subscription, sent_at, opened

---

## 🎨 Customize

**Email Template:** `motivational_quotes/templates/motivational_quotes/email/daily_quote.html`

**Subscribe Page:** `motivational_quotes/templates/motivational_quotes/subscribe.html`

**Status Page:** `motivational_quotes/templates/motivational_quotes/status.html`

---

## 🚀 Next Steps

1. ✅ Run setup commands
2. ✅ Add quotes via admin
3. ✅ Test email sending
4. ✅ Set up daily scheduler
5. ✅ Configure email SMTP
6. ✅ Deploy to production

---

**Ready to inspire? Let's go! 🚀**

Questions? See `README.md` or `SETUP_GUIDE.md`
