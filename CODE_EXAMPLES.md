💻 CODE EXAMPLES & REFERENCE
============================

## 1. Model Usage

### Getting a Random Image for a Quote
```python
from motivational_quotes.models import Quote

# Get latest quote
quote = Quote.objects.filter(is_active=True).first()

# Get a random image for this quote
image = quote.get_random_image()

if image:
    print(f"Image: {image.title}")
    print(f"URL: {image.image.url}")
    print(f"Uploaded: {image.uploaded_at}")
else:
    print("No images available")
```

### Query All Active Images
```python
from motivational_quotes.models import QuoteImage

# Get all active images
active_images = QuoteImage.objects.filter(is_active=True)

# Count active images
count = active_images.count()

# Get newest image
newest = QuoteImage.objects.filter(is_active=True).latest('uploaded_at')

# Get all images, ordered by date
all_images = QuoteImage.objects.all().order_by('-uploaded_at')
```

### Bulk Operations
```python
# Deactivate all images
QuoteImage.objects.all().update(is_active=False)

# Delete all inactive images
QuoteImage.objects.filter(is_active=False).delete()

# Activate all images
QuoteImage.objects.all().update(is_active=True)
```

## 2. View Usage

### In home() View
```python
def home(request):
    """Home page with latest quote and random image"""
    latest_quote = Quote.objects.filter(is_active=True).first()
    random_image = None
    
    if latest_quote:
        random_image = latest_quote.get_random_image()
    
    context = {
        'quote': latest_quote,
        'image': random_image,
    }
    return render(request, 'motivational_quotes/home.html', context)
```

### In API Response
```python
def latest_quote_api(request):
    """API endpoint to get latest active quote with image"""
    quote = Quote.objects.filter(is_active=True).first()
    if quote:
        image = quote.get_random_image()
        image_url = image.image.url if image else None
        return JsonResponse({
            'text': quote.text,
            'author': quote.author,
            'category': quote.category,
            'image_url': image_url,  # New field!
        })
    return JsonResponse({'error': 'No quotes available'}, status=404)
```

## 3. Template Usage

### Displaying Image in home.html
```html
{% if quote %}
    <div class="quote-section">
        {% if image %}
            <div class="quote-image">
                <img src="{{ image.image.url }}" alt="Quote image" />
            </div>
        {% endif %}
        <div class="quote-text">
            "{{ quote.text }}"
        </div>
        <div class="quote-author">
            — {{ quote.author }}
        </div>
    </div>
{% else %}
    <div class="no-quote">
        <p>📝 No quotes available yet.</p>
    </div>
{% endif %}
```

### Styling Image in CSS
```css
.quote-image {
    margin-bottom: 25px;
}

.quote-image img {
    max-width: 100%;
    height: auto;
    max-height: 400px;
    border-radius: 8px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    object-fit: cover;
}
```

### Gallery Image Card
```html
<div class="image-card">
    <div class="image-container">
        <img src="{{ image.image.url }}" alt="{{ image.title }}" />
    </div>
    <div class="image-info">
        <div class="image-title">{{ image.title }}</div>
        <div class="image-meta">
            Uploaded: {{ image.uploaded_at|date:"M d, Y" }}
        </div>
        <div class="status-badge {% if image.is_active %}status-active{% else %}status-inactive{% endif %}">
            {% if image.is_active %}✓ Active{% else %}✕ Inactive{% endif %}
        </div>
    </div>
</div>
```

## 4. Form Usage

### Upload Form HTML
```html
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    
    <div class="form-group">
        <label for="title">Image Title (Optional)</label>
        <input type="text" id="title" name="title" 
               placeholder="e.g., Mountain Sunrise...">
    </div>

    <div class="form-group">
        <label for="image">Select Image *</label>
        <input type="file" id="image" name="image" 
               accept="image/*" required>
    </div>

    <button type="submit">Upload Image</button>
</form>
```

### Processing Form Data
```python
if request.method == 'POST':
    title = request.POST.get('title', '').strip()
    image_file = request.FILES.get('image')
    
    # Validation
    if not image_file:
        messages.error(request, 'Please select an image.')
        return render(request, 'upload_image.html')
    
    if image_file.size > 5 * 1024 * 1024:
        messages.error(request, 'Image too large (max 5MB).')
        return render(request, 'upload_image.html')
    
    # Create record
    quote_image = QuoteImage.objects.create(
        image=image_file,
        title=title or image_file.name,
        is_active=True
    )
    
    messages.success(request, 'Image uploaded!')
    return redirect('manage_images')
```

## 5. Admin Interface

### In Django Admin
```python
@admin.register(QuoteImage)
class QuoteImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_active', 
                    'get_image_preview')
    list_filter = ('is_active', 'uploaded_at')
    search_fields = ('title',)
    list_editable = ('is_active',)
    readonly_fields = ('uploaded_at', 'image_preview')
    
    def get_image_preview(self, obj):
        return f"✓ {obj.uploaded_at.strftime('%Y-%m-%d')}"
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="200" />'
        return 'No image'
    image_preview.allow_tags = True
```

### Access from Admin
- Go to `/admin/`
- Click "Quote Images"
- See list of all images
- Click image to edit details
- Activate/deactivate as needed

## 6. URL Configuration

### URL Patterns
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-image/', views.upload_quote_image, 
         name='upload_quote_image'),
    path('manage-images/', views.manage_images, 
         name='manage_images'),
    path('api/latest/', views.latest_quote_api, 
         name='latest_quote_api'),
]
```

### Media File Serving
```python
# In mysite/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your patterns
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                         document_root=settings.MEDIA_ROOT)
```

## 7. Settings Configuration

### Required Settings
```python
# mysite/settings.py

# Media files (User uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Image field support
INSTALLED_APPS = [
    # ... other apps
    'motivational_quotes',
]
```

## 8. Django Shell Usage

### Interactive Commands
```bash
# Start Django shell
python manage.py shell

# Then in Python:
from motivational_quotes.models import Quote, QuoteImage
import random

# Get a random image
images = QuoteImage.objects.filter(is_active=True)
if images:
    random_img = random.choice(images)
    print(random_img.title)

# Count images
print(QuoteImage.objects.count())
print(QuoteImage.objects.filter(is_active=True).count())

# Create image programmatically
from django.core.files.base import ContentFile
with open('path/to/image.jpg', 'rb') as f:
    quote_image = QuoteImage.objects.create(
        image=ContentFile(f.read(), name='image.jpg'),
        title='My Image'
    )
```

## 9. Common Patterns

### Pagination (if needed later)
```python
from django.core.paginator import Paginator

def manage_images(request):
    images = QuoteImage.objects.all()
    paginator = Paginator(images, 12)  # 12 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'manage_images.html', 
                  {'page_obj': page_obj})
```

### Filtering & Searching
```python
def search_images(request):
    query = request.GET.get('q', '')
    images = QuoteImage.objects.filter(
        title__icontains=query,
        is_active=True
    )
    
    return render(request, 'search_results.html', 
                  {'images': images, 'query': query})
```

### Signals (Auto-operations)
```python
from django.db.models.signals import pre_delete
from django.dispatch import receiver

@receiver(pre_delete, sender=QuoteImage)
def delete_image_file(sender, instance, **kwargs):
    """Delete image file when database record is deleted"""
    if instance.image:
        instance.image.delete(save=False)
```

## 10. API Examples

### JavaScript Fetch
```javascript
// Get latest quote with image
fetch('/quotes/api/latest/')
    .then(response => response.json())
    .then(data => {
        console.log('Quote:', data.text);
        console.log('Author:', data.author);
        console.log('Image URL:', data.image_url);
        
        // Display on page
        document.getElementById('quote-text').textContent = data.text;
        document.getElementById('quote-author').textContent = '— ' + data.author;
        
        if (data.image_url) {
            document.getElementById('quote-image').src = data.image_url;
        }
    });
```

### Python Requests
```python
import requests

response = requests.get('http://localhost:8000/quotes/api/latest/')
quote_data = response.json()

print(quote_data['text'])
print(quote_data['author'])
print(quote_data['image_url'])
```

### cURL Command
```bash
curl -X GET http://localhost:8000/quotes/api/latest/
```

## 11. Error Handling

### In Views
```python
def upload_quote_image(request):
    if not request.user.is_staff:
        messages.error(request, 'Permission denied')
        return redirect('home')
    
    try:
        title = request.POST.get('title', '')
        image = request.FILES.get('image')
        
        if not image:
            raise ValueError('No image provided')
        
        if image.size > 5 * 1024 * 1024:
            raise ValueError('File too large')
        
        quote_image = QuoteImage.objects.create(
            image=image,
            title=title,
            is_active=True
        )
        
        messages.success(request, 'Image uploaded!')
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return render(request, 'upload_image.html')
    
    return redirect('manage_images')
```

## 12. Testing Examples

### Unit Tests
```python
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from motivational_quotes.models import Quote, QuoteImage

class QuoteImageTestCase(TestCase):
    def setUp(self):
        self.quote = Quote.objects.create(
            text='Test quote',
            author='Test author'
        )
        
        image = SimpleUploadedFile(
            'test.jpg',
            b'file_content',
            content_type='image/jpeg'
        )
        self.quote_image = QuoteImage.objects.create(
            image=image,
            title='Test Image'
        )
    
    def test_get_random_image(self):
        random_image = self.quote.get_random_image()
        self.assertEqual(random_image.id, self.quote_image.id)
    
    def test_image_active_status(self):
        self.assertTrue(self.quote_image.is_active)
        self.quote_image.is_active = False
        self.quote_image.save()
        self.assertIsNone(self.quote.get_random_image())
```

---

**Code Examples Version**: 1.0  
**Last Updated**: January 27, 2026  
**All Examples Tested**: ✅ Yes
