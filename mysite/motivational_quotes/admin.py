from django.contrib import admin
from .models import Quote, Subscription, SentQuote, QuoteImage


@admin.register(QuoteImage)
class QuoteImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_active', 'get_image_preview')
    list_filter = ('is_active', 'uploaded_at')
    search_fields = ('title',)
    list_editable = ('is_active',)
    readonly_fields = ('uploaded_at', 'image_preview')

    def get_image_preview(self, obj):
        return f"✓ {obj.uploaded_at.strftime('%Y-%m-%d')}"
    get_image_preview.short_description = 'Preview'

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="200" />'
        return 'No image'
    image_preview.allow_tags = True


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('get_short_text', 'author', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('text', 'author')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Quote Content', {
            'fields': ('text', 'author', 'category')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_short_text(self, obj):
        return obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
    get_short_text.short_description = 'Quote'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'is_active', 'preferred_time', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('user__username', 'email')
    list_editable = ('is_active', 'preferred_time')
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'email')
        }),
        ('Preferences', {
            'fields': ('preferred_time', 'is_active')
        }),
        ('Subscription History', {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SentQuote)
class SentQuoteAdmin(admin.ModelAdmin):
    list_display = ('get_quote_preview', 'get_user', 'sent_at', 'opened')
    list_filter = ('sent_at', 'opened')
    search_fields = ('quote__text', 'subscription__user__username')
    readonly_fields = ('sent_at', 'quote', 'subscription')
    list_editable = ('opened',)

    def get_quote_preview(self, obj):
        return obj.quote.text[:50] + '...'
    get_quote_preview.short_description = 'Quote'

    def get_user(self, obj):
        return obj.subscription.user.username
    get_user.short_description = 'User'
