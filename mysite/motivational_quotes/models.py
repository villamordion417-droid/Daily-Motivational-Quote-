from django.db import models
from django.contrib.auth.models import User
import random


class QuoteImage(models.Model):
    """Store uploaded images for random attachment to quotes"""
    image = models.ImageField(
        upload_to='quote_images/',
        help_text="Upload an image to be randomly attached to quotes"
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional title for this image"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Use this image for random selection")

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = "Quote Images"

    def __str__(self):
        return f"{self.title or 'Image'} - {self.uploaded_at.strftime('%Y-%m-%d')}"


class Quote(models.Model):
    """Store motivational quotes"""
    text = models.TextField(help_text="The quote text")
    author = models.CharField(max_length=255, blank=True, help_text="Author of the quote")
    category = models.CharField(
        max_length=50,
        choices=[
            ('motivation', 'Motivation'),
            ('success', 'Success'),
            ('perseverance', 'Perseverance'),
            ('courage', 'Courage'),
            ('inspiration', 'Inspiration'),
            ('growth', 'Growth'),
            ('wisdom', 'Wisdom'),
        ],
        default='motivation'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Include in daily send")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Quotes"

    def __str__(self):
        return f'"{self.text[:50]}..." - {self.author}'

    def get_random_image(self):
        """Get a random active image for this quote"""
        active_images = QuoteImage.objects.filter(is_active=True)
        if not active_images.exists():
            return None
        return random.choice(active_images)


class Subscription(models.Model):
    """Track user subscriptions for daily quotes"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='quote_subscription')
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    preferred_time = models.TimeField(
        default='08:00',
        help_text="Preferred time to receive quotes (HH:MM format)"
    )

    class Meta:
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f'{self.user.username} - {self.email}'


class SentQuote(models.Model):
    """Track sent quotes for analytics"""
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='sent_instances')
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f'Quote {self.quote.id} sent to {self.subscription.user.username}'
