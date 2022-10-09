from django.test import SimpleTestCase


class HomePageCase(SimpleTestCase):
    def test_index_loads_properly(self):
        """THE index page loads properly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
