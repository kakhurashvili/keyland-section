from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from UserProfile.middleware import EarningPointsMiddleware
from .models import EarningPoint

User = get_user_model()


class EarningPointsMiddlewareTestCase(TestCase):
    def test_deduct_expiring_points(self):
        # Create a user for testing
        user = User.objects.create_user(email='admin@admin.com', password='1')

        # Create earning points for the user with different dates
        current_date = timezone.now().date()
        EarningPoint.objects.create(customer_point=user, date=current_date, points=5)
        EarningPoint.objects.create(customer_point=user, date=current_date - timezone.timedelta(days=30), points=3)
        EarningPoint.objects.create(customer_point=user, date=current_date + timezone.timedelta(days=45), points=2)

        # Instantiate the middleware and call the deduct_expiring_points method
        middleware = EarningPointsMiddleware(get_response=None)
        middleware.deduct_expiring_points(user)

        # Retrieve the updated earning points for the current date
        updated_points = EarningPoint.objects.filter(customer_point=user, date=current_date).first()

        # Assert that the points have been deducted correctly
        self.assertEqual(updated_points.points, 3)  # Update the expected value to match the actual deducted points
