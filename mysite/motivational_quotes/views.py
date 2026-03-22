from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Subscription, Quote, QuoteImage


def home(request):
    """Home page with latest quote and random image - no login required"""
    try:
        latest_quote = Quote.objects.filter(is_active=True).first()
        random_image = None
        
        if latest_quote:
            random_image = latest_quote.get_random_image()
    except Exception as e:
        latest_quote = None
        random_image = None
    
    context = {
        'quote': latest_quote,
        'image': random_image,
    }
    return render(request, 'motivational_quotes/home.html', context)


def subscribe_to_quotes(request):
    """Subscribe to daily motivational quotes - no login required"""
    if request.method == 'POST':
        try:
            email = request.POST.get('email', '').strip()
            
            if not email:
                messages.error(request, 'Please enter a valid email address.')
                return render(request, 'motivational_quotes/subscribe.html')
            
            # For anonymous users, create a subscription with email only
            if request.user.is_authenticated:
                subscription, created = Subscription.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'email': request.user.email,
                        'is_active': True
                    }
                )
                
                if not created and not subscription.is_active:
                    subscription.is_active = True
                    subscription.unsubscribed_at = None
                    subscription.save()
                    messages.success(request, 'You have been resubscribed to daily quotes!')
                elif created:
                    messages.success(request, 'You are now subscribed to daily motivational quotes!')
                else:
                    messages.info(request, 'You are already subscribed to daily quotes.')
                
                return redirect('quote_subscription_status')
            else:
                # For anonymous users, check if email already subscribed
                subscription = Subscription.objects.filter(email=email, is_active=True).first()
                if subscription:
                    messages.info(request, f'Email {email} is already subscribed!')
                    return render(request, 'motivational_quotes/subscribe.html')
                
                # Create subscription for anonymous user
                from django.contrib.auth.models import User
                # Try to find or create a user for this email
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={'username': email.split('@')[0]}
                )
                
                subscription, created = Subscription.objects.get_or_create(
                    user=user,
                    defaults={
                        'email': email,
                        'is_active': True
                    }
                )
                
                if not subscription.is_active:
                    subscription.is_active = True
                    subscription.unsubscribed_at = None
                    subscription.save()
                
                messages.success(request, f'✅ {email} is now subscribed to daily quotes!')
                return render(request, 'motivational_quotes/subscribe.html')
        except Exception as e:
            messages.error(request, f'Error subscribing: {str(e)}')
            return render(request, 'motivational_quotes/subscribe.html')
    
    return render(request, 'motivational_quotes/subscribe.html')


@login_required
def unsubscribe_from_quotes(request):
    """Unsubscribe user from daily motivational quotes"""
    if request.method == 'POST':
        try:
            subscription = Subscription.objects.get(user=request.user)
            subscription.is_active = False
            from django.utils import timezone
            subscription.unsubscribed_at = timezone.now()
            subscription.save()
            messages.success(request, 'You have been unsubscribed from daily quotes.')
            return redirect('quote_subscription_status')
        except Subscription.DoesNotExist:
            messages.warning(request, 'You are not currently subscribed.')
            return redirect('quote_subscription_status')
    
    return render(request, 'motivational_quotes/unsubscribe.html')


@login_required
def subscription_status(request):
    """View subscription status and settings"""
    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        subscription = None
    
    context = {
        'subscription': subscription,
        'latest_quote': Quote.objects.filter(is_active=True).first(),
    }
    return render(request, 'motivational_quotes/status.html', context)


@login_required
def update_preferred_time(request):
    """Update preferred time for receiving quotes"""
    if request.method == 'POST':
        time = request.POST.get('preferred_time')
        try:
            subscription, _ = Subscription.objects.get_or_create(
                user=request.user,
                defaults={'email': request.user.email}
            )
            subscription.preferred_time = time
            subscription.save()
            messages.success(request, f'Preferred time updated to {time}')
            return redirect('quote_subscription_status')
        except Exception as e:
            messages.error(request, f'Error updating time: {str(e)}')
            return redirect('quote_subscription_status')
    
    return redirect('quote_subscription_status')


def latest_quote_api(request):
    """API endpoint to get latest active quote"""
    quote = Quote.objects.filter(is_active=True).first()
    if quote:
        image = quote.get_random_image()
        image_url = image.image.url if image else None
        return JsonResponse({
            'text': quote.text,
            'author': quote.author,
            'category': quote.category,
            'image_url': image_url,
        })
    return JsonResponse({'error': 'No quotes available'}, status=404)


@login_required
def upload_quote_image(request):
    """Upload a new image for quotes - Admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to upload images.')
        return redirect('home')
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            image_file = request.FILES.get('image')
            
            if not image_file:
                messages.error(request, 'Please select an image to upload.')
                return render(request, 'motivational_quotes/upload_image.html')
            
            # Check file size (max 5MB)
            if image_file.size > 5 * 1024 * 1024:
                messages.error(request, 'Image size must be less than 5MB.')
                return render(request, 'motivational_quotes/upload_image.html')
            
            # Create and save the image
            quote_image = QuoteImage.objects.create(
                image=image_file,
                title=title or image_file.name,
                is_active=True
            )
            
            messages.success(request, f'✅ Image "{quote_image.title}" uploaded successfully!')
            return redirect('manage_images')
            
        except Exception as e:
            messages.error(request, f'Error uploading image: {str(e)}')
            return render(request, 'motivational_quotes/upload_image.html')
    
    return render(request, 'motivational_quotes/upload_image.html')


def admin_redirect(request):
    """Redirect /admin/ to in-app quotes manager for staff users."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('manage_quotes')
    # If not staff, redirect to existing Django admin login with a message.
    messages.info(request, 'Please log in as staff to access quote management.')
    return redirect('django_admin:login')


@login_required
def manage_images(request):
    """Manage uploaded images - Admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        action = request.POST.get('action')
        
        try:
            quote_image = QuoteImage.objects.get(id=image_id)
            
            if action == 'delete':
                image_title = quote_image.title
                quote_image.delete()
                messages.success(request, f'✅ Image "{image_title}" deleted successfully!')
            elif action == 'toggle':
                quote_image.is_active = not quote_image.is_active
                quote_image.save()
                status = 'activated' if quote_image.is_active else 'deactivated'
                messages.success(request, f'✅ Image "{quote_image.title}" {status}!')
        except QuoteImage.DoesNotExist:
            messages.error(request, 'Image not found.')
        except Exception as e:
            messages.error(request, f'Error managing image: {str(e)}')
    
    images = QuoteImage.objects.all()
    context = {
        'images': images,
        'total_images': images.count(),
        'active_images': images.filter(is_active=True).count(),
    }
    
    return render(request, 'motivational_quotes/manage_images.html', context)


@login_required
def manage_quotes(request):
    """Manage motivational quotes - Admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    if request.method == 'POST':
        quote_id = request.POST.get('quote_id')
        action = request.POST.get('action')

        try:
            if action == 'create':
                text = request.POST.get('quote_text', '').strip()
                author = request.POST.get('quote_author', '').strip()
                category = request.POST.get('quote_category', '').strip() or 'motivation'

                if not text:
                    raise ValueError('Quote text cannot be empty.')

                Quote.objects.create(text=text, author=author, category=category, is_active=True)
                messages.success(request, '✅ Quote added successfully!')

            elif quote_id:
                quote = Quote.objects.get(id=quote_id)

                if action == 'delete':
                    quote.delete()
                    messages.success(request, '✅ Quote deleted successfully!')
                elif action == 'toggle':
                    quote.is_active = not quote.is_active
                    quote.save()
                    status = 'activated' if quote.is_active else 'deactivated'
                    messages.success(request, f'✅ Quote {status}!')

        except Quote.DoesNotExist:
            messages.error(request, 'Quote not found.')
        except Exception as e:
            messages.error(request, f'Error managing quote: {str(e)}')

    quotes = Quote.objects.all()
    context = {
        'quotes': quotes,
        'total_quotes': quotes.count(),
        'active_quotes': quotes.filter(is_active=True).count(),
    }

    return render(request, 'motivational_quotes/manage_quotes.html', context)


@login_required
def manage_subscribers(request):
    """Manage subscribers - Admin only"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    if request.method == 'POST':
        subscriber_id = request.POST.get('subscriber_id')
        action = request.POST.get('action')

        try:
            subscriber = Subscription.objects.get(id=subscriber_id)

            if action == 'deactivate':
                subscriber.is_active = False
                subscriber.unsubscribed_at = timezone.now()
                subscriber.save()
                messages.success(request, f'✅ Subscriber "{subscriber.user.username}" deactivated!')
            elif action == 'activate':
                subscriber.is_active = True
                subscriber.unsubscribed_at = None
                subscriber.save()
                messages.success(request, f'✅ Subscriber "{subscriber.user.username}" activated!')
            elif action == 'delete':
                username = subscriber.user.username
                subscriber.delete()
                messages.success(request, f'✅ Subscriber "{username}" deleted!')

        except Subscription.DoesNotExist:
            messages.error(request, 'Subscriber not found.')
        except Exception as e:
            messages.error(request, f'Error managing subscriber: {str(e)}')

    subscribers = Subscription.objects.all().select_related('user')
    context = {
        'subscribers': subscribers,
        'total_subscribers': subscribers.count(),
        'active_subscribers': subscribers.filter(is_active=True).count(),
    }

    return render(request, 'motivational_quotes/manage_subscribers.html', context)
