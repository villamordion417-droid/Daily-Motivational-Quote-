from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import datetime
import random

from mysite.motivational_quotes.models import Quote, Subscription, SentQuote


class Command(BaseCommand):
    help = 'Send daily motivational quotes to all active subscribers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Send to all subscribers regardless of preferred time',
        )

    def handle(self, *args, **options):
        # Get all active subscriptions
        subscriptions = Subscription.objects.filter(is_active=True)
        
        if not subscriptions.exists():
            self.stdout.write(self.style.WARNING('No active subscriptions found.'))
            return

        # Get a random active quote
        quotes = Quote.objects.filter(is_active=True)
        if not quotes.exists():
            self.stdout.write(self.style.ERROR('No active quotes found. Please add quotes first.'))
            return

        quote = quotes.order_by('?').first()

        current_time = timezone.now().time()
        sent_count = 0
        failed_count = 0

        for subscription in subscriptions:
            # Check if current time matches preferred time (or send all if --all flag)
            if options['all'] or current_time.hour == subscription.preferred_time.hour:
                try:
                    # Prepare email content
                    subject = 'Your Daily Motivational Quote'
                    html_message = self._render_email(quote, subscription.user.first_name or subscription.user.username)
                    text_message = f'{quote.text}\n\n- {quote.author}'

                    # Send email
                    send_mail(
                        subject,
                        text_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [subscription.email],
                        html_message=html_message,
                        fail_silently=False,
                    )

                    # Log sent quote
                    SentQuote.objects.create(
                        quote=quote,
                        subscription=subscription,
                    )

                    sent_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Sent to {subscription.email}')
                    )

                except Exception as e:
                    failed_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to send to {subscription.email}: {str(e)}')
                    )

        # Summary
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Daily quote sending complete!\n'
                f'Successfully sent: {sent_count}\n'
                f'Failed: {failed_count}'
            )
        )

    def _render_email(self, quote, user_name='Friend'):
        """Render HTML email template"""
        context = {
            'quote': quote,
            'user_name': user_name,
        }
        return render_to_string('motivational_quotes/email/daily_quote.html', context)
