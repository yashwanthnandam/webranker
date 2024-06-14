from django.test import TestCase
from urlranker.entities import Link

class LinkTestCase(TestCase):
    def test_link_is_valid(self):
        valid_link = Link("Valid Text", "http://example.com")
        self.assertTrue(valid_link.is_valid())

        invalid_link = Link("Past week", "http://example.com")
        self.assertFalse(invalid_link.is_valid())

        google_link = Link("Google link", "http://google.com")
        self.assertFalse(google_link.is_valid())
