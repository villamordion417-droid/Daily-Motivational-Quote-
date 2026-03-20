📐 SYSTEM ARCHITECTURE - QUOTE IMAGE SYSTEM
==========================================

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  home.html   │  │upload_image. │  │manage_images │      │
│  │   (Display)  │  │   html       │  │    .html     │      │
│  │  Quote +     │  │ (Form)       │  │ (Gallery)    │      │
│  │  Image       │  │              │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LOGIC LAYER                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Views (views.py):                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • home() - Display quote + random image              │   │
│  │ • upload_quote_image() - Handle image upload         │   │
│  │ • manage_images() - Manage image gallery             │   │
│  │ • latest_quote_api() - API with image URL            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                      DATA MODEL LAYER                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Models (models.py):                                        │
│  ┌──────────────────────┐  ┌──────────────────────────┐   │
│  │   Quote Model        │  │  QuoteImage Model        │   │
│  ├──────────────────────┤  ├──────────────────────────┤   │
│  │ • id (PK)            │  │ • id (PK)                │   │
│  │ • text               │  │ • image (ImageField)     │   │
│  │ • author             │  │ • title                  │   │
│  │ • category           │  │ • uploaded_at            │   │
│  │ • is_active          │  │ • is_active              │   │
│  │ • created_at         │  └──────────────────────────┘   │
│  │ • updated_at         │                                  │
│  │ • get_random_image() │  Related:                       │
│  └──────────────────────┘  Quote ← random → QuoteImage    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    DATABASE LAYER (SQLite)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────┐  ┌─────────────────────────────┐ │
│  │ motivational_quotes │  │ motivational_quotes_        │ │
│  │      _quote         │  │    quoteimage               │ │
│  ├─────────────────────┤  ├─────────────────────────────┤ │
│  │ id (PK)             │  │ id (PK)                     │ │
│  │ text                │  │ image (path/filename)       │ │
│  │ author              │  │ title                       │ │
│  │ category            │  │ uploaded_at                 │ │
│  │ is_active           │  │ is_active                   │ │
│  │ created_at          │  └─────────────────────────────┘ │
│  │ updated_at          │                                   │
│  └─────────────────────┘                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    FILE STORAGE LAYER                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  mysite/media/quote_images/                                 │
│  ├── image_001.jpg                                          │
│  ├── image_002.png                                          │
│  ├── mountain_sunrise.jpg                                   │
│  └── ... (all uploaded images)                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Request Flow Diagram

### 1. User Views Home Page
```
Browser Request
    ↓
Django Router (/quotes/)
    ↓
home() view
    ↓
Get latest active Quote
    ↓
Call quote.get_random_image()
    ↓
Random select from QuoteImage.objects.filter(is_active=True)
    ↓
Pass to template: {'quote': quote, 'image': random_image}
    ↓
Render home.html with quote + image
    ↓
Return HTML to Browser
```

### 2. User Uploads Image
```
Browser uploads form
    ↓
Django Router (/quotes/upload-image/)
    ↓
upload_quote_image() view
    ↓
Check: User is staff?
    ↓
Validate file: size < 5MB, format OK?
    ↓
Create QuoteImage record
    ↓
Save to: media/quote_images/{filename}
    ↓
Redirect to manage_images
    ↓
Show success message
```

### 3. User Manages Images
```
Browser navigates to /quotes/manage-images/
    ↓
Django Router
    ↓
manage_images() view
    ↓
Check: User is staff?
    ↓
Get all QuoteImage objects
    ↓
Render manage_images.html
    ↓
Show gallery with images
    ↓
User can: activate, deactivate, delete
    ↓
POST back with image_id + action
    ↓
Update database
    ↓
Show success/error message
```

## Component Relationships

```
┌─────────────────────────────────────────────────────────┐
│                   URLS & ROUTING                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  /quotes/                    → home()                   │
│  /quotes/upload-image/       → upload_quote_image()    │
│  /quotes/manage-images/      → manage_images()         │
│  /quotes/api/latest/         → latest_quote_api()      │
│  /quotes/subscribe/          → subscribe_to_quotes()   │
│  /quotes/unsubscribe/        → unsubscribe...()        │
│  /quotes/status/             → subscription_status()   │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                   VIEWS & HANDLERS                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  home()                                                 │
│    ├─ Query: Quote.objects.filter(is_active=True)     │
│    ├─ Call: quote.get_random_image()                  │
│    ├─ Query: QuoteImage.objects.filter(is_active=True)│
│    └─ Render: home.html                               │
│                                                         │
│  upload_quote_image()                                   │
│    ├─ Check: @login_required, is_staff               │
│    ├─ Validate: file size, format                     │
│    ├─ Create: QuoteImage object                       │
│    ├─ Save: to media/quote_images/                    │
│    └─ Redirect: manage_images()                       │
│                                                         │
│  manage_images()                                        │
│    ├─ Check: @login_required, is_staff               │
│    ├─ Query: QuoteImage.objects.all()                 │
│    ├─ Handle: POST with action (toggle/delete)        │
│    └─ Render: manage_images.html                      │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         ↕
┌─────────────────────────────────────────────────────────┐
│                   MODELS & DATABASE                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Quote.objects.filter(is_active=True)                  │
│    ↓                                                    │
│  selected_quote.get_random_image()                     │
│    ↓                                                    │
│  QuoteImage.objects.filter(is_active=True)            │
│    ↓                                                    │
│  random.choice(active_images)                          │
│    ↓                                                    │
│  Return QuoteImage instance                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Data Flow for Image Display

```
┌──────────────────┐
│  User visits     │
│  /quotes/home    │
└────────┬─────────┘
         │
         ↓
┌──────────────────────────────────────┐
│  home() view executes                │
│  1. Get latest Quote                 │
│  2. Call quote.get_random_image()    │
└────────┬─────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────┐
│  Database Queries:                   │
│  1. SELECT * FROM quote              │
│     WHERE is_active = TRUE           │
│     ORDER BY created_at DESC         │
│     LIMIT 1                          │
└────────┬─────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────┐
│  2. SELECT * FROM quoteimage         │
│     WHERE is_active = TRUE           │
└────────┬─────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────┐
│  Python Logic:                       │
│  if active_images exist:             │
│      return random.choice(list)      │
│  else:                               │
│      return None                     │
└────────┬─────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────┐
│  Template Rendering (home.html):     │
│  {% if image %}                      │
│    <img src="{{ image.image.url }}"  │
│  {% endif %}                         │
└────────┬─────────────────────────────┘
         │
         ↓
┌──────────────────────────────────────┐
│  Browser Display:                    │
│  Shows:                              │
│  - Quote text                        │
│  - Quote author                      │
│  - Random image above quote          │
└──────────────────────────────────────┘
```

## Class Hierarchy

```
Django Model
  │
  ├─ Quote (existing)
  │  ├─ TextField: text
  │  ├─ CharField: author
  │  ├─ CharField: category
  │  ├─ DateTimeField: created_at
  │  ├─ DateTimeField: updated_at
  │  ├─ BooleanField: is_active
  │  └─ Method: get_random_image() ← NEW
  │
  └─ QuoteImage (NEW)
     ├─ ImageField: image
     ├─ CharField: title
     ├─ DateTimeField: uploaded_at
     └─ BooleanField: is_active


Django ModelAdmin
  │
  ├─ QuoteAdmin (existing)
  └─ QuoteImageAdmin (NEW) ← NEW
     ├─ list_display
     ├─ list_filter
     ├─ search_fields
     ├─ readonly_fields
     └─ image_preview() ← NEW
```

## Permission & Access Control

```
┌─────────────────────────────────────┐
│    Public Views (No Login)           │
├─────────────────────────────────────┤
│  • GET /quotes/                      │
│    View home page with quotes        │
│  • GET /quotes/subscribe/            │
│    View subscribe form               │
│  • POST /quotes/subscribe/           │
│    Submit subscription               │
│  • GET /quotes/api/latest/           │
│    Get latest quote as JSON          │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Staff-Only Views (Login Required)   │
├─────────────────────────────────────┤
│  • GET /quotes/upload-image/         │
│    View upload form                  │
│  • POST /quotes/upload-image/        │
│    Upload new image                  │
│  • GET /quotes/manage-images/        │
│    View image gallery                │
│  • POST /quotes/manage-images/       │
│    Activate/deactivate/delete images │
│  • GET /admin/                       │
│    Django admin panel                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Authenticated User Views            │
├─────────────────────────────────────┤
│  • GET /quotes/subscribe/            │
│    Subscribe with email              │
│  • GET /quotes/status/               │
│    View subscription status          │
│  • POST /quotes/update-time/         │
│    Change preferred time             │
└─────────────────────────────────────┘
```

## Technology Stack

```
┌──────────────────────────────────────┐
│         PRESENTATION LAYER            │
├──────────────────────────────────────┤
│ • HTML5 Templates                    │
│ • CSS3 (Inline + Responsive)         │
│ • Django Template Language            │
│ • Media file serving (/media/)       │
└──────────────────────────────────────┘
         ↑
┌──────────────────────────────────────┐
│      APPLICATION LAYER                │
├──────────────────────────────────────┤
│ • Django 6.0.1 Framework              │
│ • Python 3.13.6                       │
│ • Class-Based & Function Views        │
│ • Form Handling & Validation           │
│ • Authentication System                │
└──────────────────────────────────────┘
         ↑
┌──────────────────────────────────────┐
│         DATA LAYER                   │
├──────────────────────────────────────┤
│ • Django ORM                          │
│ • SQLite 3 Database                   │
│ • Model Relationships                 │
│ • Query Optimization                  │
└──────────────────────────────────────┘
         ↑
┌──────────────────────────────────────┐
│       STORAGE LAYER                  │
├──────────────────────────────────────┤
│ • Pillow 10.0.0 (Image Processing)   │
│ • File System Storage                 │
│ • Media Directory Management           │
│ • Image Format Support                │
└──────────────────────────────────────┘
```

## Performance Characteristics

```
Operation              Complexity    Notes
──────────────────────────────────────────────────
Get random image       O(n)          n = active images
Display home page      O(1) + O(n)   1 quote + 1 random
Upload image           O(1)          Single insert
List all images        O(m)          m = total images
Activate/Deactivate    O(1)          Single update
Delete image           O(1)          Single delete

Database Indexes:
• Primary Keys (id)
• Foreign Keys (if added)
• is_active (for filtering)
```

---

**Architecture Document Version**: 1.0  
**Last Updated**: January 27, 2026  
**Status**: Production Ready ✅
