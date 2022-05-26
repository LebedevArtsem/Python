from django.test import TestCase, Client
from django.urls import reverse


class ViewsTestCase(TestCase):
    def setUp(self):
        pass

    def test_index(self):
        client = Client()
        response = client.get(reverse(''))
        self.assertTemplateUsed(response, 'store/index.html')
