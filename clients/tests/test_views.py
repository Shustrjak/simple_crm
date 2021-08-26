from django.test import TestCase
from django.shortcuts import reverse


class PageViewTest(TestCase):

    def test_landing_page_get(self):
        response = self.client.get(reverse("landing-page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing.html")
