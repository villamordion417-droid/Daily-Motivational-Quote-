"""
Script to populate the database with sample motivational quotes.
Run with: cd mysite && python manage.py shell < ../populate_quotes.py
"""

import os
import sys
import django

# Add mysite directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mysite'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from mysite.motivational_quotes.models import Quote

# Sample quotes to add
QUOTES = [
    {
        "text": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "category": "success",
    },
    {
        "text": "Believe you can and you're halfway there.",
        "author": "Theodore Roosevelt",
        "category": "motivation",
    },
    {
        "text": "Success is not final, failure is not fatal.",
        "author": "Winston Churchill",
        "category": "perseverance",
    },
    {
        "text": "Don't watch the clock; do what it does. Keep going.",
        "author": "Sam Levenson",
        "category": "motivation",
    },
    {
        "text": "The future belongs to those who believe in the beauty of their dreams.",
        "author": "Eleanor Roosevelt",
        "category": "inspiration",
    },
    {
        "text": "It is during our darkest moments that we must focus to see the light.",
        "author": "Aristotle",
        "category": "wisdom",
    },
    {
        "text": "The only impossible journey is the one you never begin.",
        "author": "Tony Robbins",
        "category": "motivation",
    },
    {
        "text": "Great things never come from comfort zones.",
        "author": "Unknown",
        "category": "growth",
    },
    {
        "text": "Dream bigger. Do bigger.",
        "author": "Robin Sharma",
        "category": "inspiration",
    },
    {
        "text": "Success is walking from failure to failure with no loss of enthusiasm.",
        "author": "Winston Churchill",
        "category": "perseverance",
    },
    {
        "text": "The expert in anything was once a beginner.",
        "author": "Helen Hayes",
        "category": "growth",
    },
    {
        "text": "Your limitation—it's only your imagination. Push yourself.",
        "author": "Unknown",
        "category": "motivation",
    },
    {
        "text": "Great success is built on failure, frustration, even catastrophe.",
        "author": "Arianna Huffington",
        "category": "success",
    },
    {
        "text": "You don't have to be great to start, but you have to start to be great.",
        "author": "Zig Ziglar",
        "category": "motivation",
    },
    {
        "text": "Courage is being scared to death, but saddling up anyway.",
        "author": "John Wayne",
        "category": "courage",
    },
    {
        "text": "The moment you doubt whether you can fly, you cease forever to be able to do it.",
        "author": "J.M. Barrie",
        "category": "inspiration",
    },
    {
        "text": "Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine.",
        "author": "Roy T. Bennett",
        "category": "motivation",
    },
    {
        "text": "I am not afraid of storms, for I am learning how to sail my ship.",
        "author": "Louisa May Alcott",
        "category": "courage",
    },
    {
        "text": "The best time to plant a tree was 20 years ago. The second best time is now.",
        "author": "Chinese Proverb",
        "category": "wisdom",
    },
    {
        "text": "Your biggest limitation is you.",
        "author": "Unknown",
        "category": "growth",
    },
]

# Add quotes to database
for quote_data in QUOTES:
    quote, created = Quote.objects.get_or_create(
        text=quote_data["text"],
        defaults={
            "author": quote_data["author"],
            "category": quote_data["category"],
            "is_active": True,
        },
    )
    if created:
        print(f"✓ Added: {quote_data['text'][:50]}...")
    else:
        print(f"- Already exists: {quote_data['text'][:50]}...")

print(f"\n✓ Total quotes in database: {Quote.objects.count()}")
