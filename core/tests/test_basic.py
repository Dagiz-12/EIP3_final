from django.test import TestCase, Client
from django.urls import reverse


class BasicFunctionalityTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        """Test that home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        """Test contact page loads"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_admin_access(self):
        """Test admin login page loads"""
        response = self.client.get('/admin/')
        # Should redirect to login (302) or show login page (200)
        self.assertIn(response.status_code, [200, 302])

    def test_static_files_config(self):
        """Test static files configuration"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertTrue(hasattr(settings, 'STATIC_ROOT'))

    def test_media_files_config(self):
        """Test media files configuration"""
        from django.conf import settings
        self.assertTrue(hasattr(settings, 'MEDIA_URL'))
        self.assertTrue(hasattr(settings, 'MEDIA_ROOT'))
