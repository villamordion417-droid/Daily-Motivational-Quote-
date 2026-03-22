from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.subscribe_to_quotes, name='subscribe_quotes'),
    path('unsubscribe/', views.unsubscribe_from_quotes, name='unsubscribe_quotes'),
    path('status/', views.subscription_status, name='quote_subscription_status'),
    path('update-time/', views.update_preferred_time, name='update_quote_time'),
    path('api/latest/', views.latest_quote_api, name='latest_quote_api'),
    path('upload-image/', views.upload_quote_image, name='upload_quote_image'),
    path('manage-images/', views.manage_images, name='manage_images'),
    path('manage/', views.manage_quotes, name='manage_quotes'),
    path('manage-subscribers/', views.manage_subscribers, name='manage_subscribers'),
]
