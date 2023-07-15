from django.test import TestCase, Client
from core.models import User
from django.urls import reverse
from storeapp.models import Product, SavedItem

class AddSavedItemsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='test@test.ge', password='testpassword')
        self.product = Product.objects.create(name='apple2', slug='apple2')

    def test_add_saved_items(self):
        self.client.login(email='test@test.ge', password='testpassword')

        url = reverse('addSavedItems')  # Replace with the actual URL name
        data = {'counter': 0, 'd': self.product.sku}  # Provide valid JSON data
        response = self.client.post(url, data=data)
        # Continue with your assertions and assertions for the response

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 1)

        # Assert that the SavedItem object was created with the correct values
        saved_item = SavedItem.objects.get(owner=self.user.customer, product=self.product)
        self.assertEqual(saved_item.added, 1)

        # Test the case where counter is 0
        data['counter'] = 0
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 0)

        # Assert that the SavedItem object was deleted
        self.assertFalse(SavedItem.objects.filter(owner=self.user.customer, product=self.product).exists())
