from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from motivational_quotes.models import Quote, Subscription, SentQuote
from django.utils import timezone


class QuoteModelTest(TestCase):
    """Test Quote model"""
    
    def setUp(self):
        self.quote = Quote.objects.create(
            text="Test quote text",
            author="Test Author",
            category="motivation",
            is_active=True
        )
    
    def test_quote_creation(self):
        """Test creating a quote"""
        self.assertEqual(self.quote.text, "Test quote text")
        self.assertEqual(self.quote.author, "Test Author")
        self.assertTrue(self.quote.is_active)
    
    def test_quote_str(self):
        """Test quote string representation"""
        expected = '"Test quote text"... - Test Author'
        self.assertEqual(str(self.quote), expected)


class SubscriptionModelTest(TestCase):
    """Test Subscription model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            email='test@example.com',
            is_active=True
        )
    
    def test_subscription_creation(self):
        """Test creating a subscription"""
        self.assertEqual(self.subscription.user.username, 'testuser')
        self.assertTrue(self.subscription.is_active)
    
    def test_subscription_str(self):
        """Test subscription string representation"""
        expected = 'testuser - test@example.com'
        self.assertEqual(str(self.subscription), expected)


class SubscribeViewTest(TestCase):
    """Test subscription views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_subscribe_page_load(self):
        """Test subscribe page loads"""
        response = self.client.get(reverse('subscribe_quotes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'motivational_quotes/subscribe.html')
    
    def test_subscribe_user(self):
        """Test user subscription"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('subscribe_quotes'))
        
        # Check redirect to status page
        self.assertEqual(response.status_code, 302)
        
        # Check subscription created
        subscription = Subscription.objects.get(user=self.user)
        self.assertTrue(subscription.is_active)
    
    def test_unsubscribe_user(self):
        """Test user unsubscribe"""
        # Create subscription first
        subscription = Subscription.objects.create(
            user=self.user,
            email='test@example.com',
            is_active=True
        )
        
        # Unsubscribe
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('unsubscribe_quotes'))
        
        # Check subscription deactivated
        subscription.refresh_from_db()
        self.assertFalse(subscription.is_active)
        self.assertIsNotNone(subscription.unsubscribed_at)


class StatusViewTest(TestCase):
    """Test subscription status view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_status_page_requires_login(self):
        """Test status page requires authentication"""
        response = self.client.get(reverse('quote_subscription_status'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_status_page_load(self):
        """Test status page loads for logged in user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quote_subscription_status'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'motivational_quotes/status.html')


class SendDailyQuoteTest(TestCase):
    """Test send_daily_quote command"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.subscription = Subscription.objects.create(
            user=self.user,
            email='test@example.com',
            is_active=True
        )
        self.quote = Quote.objects.create(
            text="Test quote",
            author="Test Author",
            is_active=True
        )
    
    def test_quote_selection(self):
        """Test that quotes are selected properly"""
        quotes = Quote.objects.filter(is_active=True)
        self.assertEqual(quotes.count(), 1)
        self.assertEqual(quotes.first().text, "Test quote")
    
    def test_subscription_filtering(self):
        """Test that subscriptions are filtered correctly"""
        active_subs = Subscription.objects.filter(is_active=True)
        self.assertEqual(active_subs.count(), 1)
        self.assertEqual(active_subs.first().user.username, 'testuser')


class LatestQuoteAPITest(TestCase):
    """Test REST API endpoint"""
    
    def setUp(self):
        self.quote = Quote.objects.create(
            text="API test quote",
            author="Test Author",
            category="motivation",
            is_active=True
        )
    
    def test_api_returns_quote(self):
        """Test API returns latest quote"""
        response = self.client.get(reverse('latest_quote_api'))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['text'], "API test quote")
        self.assertEqual(data['author'], "Test Author")
    
    def test_api_no_quotes(self):
        """Test API when no quotes available"""
        Quote.objects.all().delete()
        response = self.client.get(reverse('latest_quote_api'))
        self.assertEqual(response.status_code, 404)
