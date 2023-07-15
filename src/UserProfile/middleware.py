from datetime import datetime, timedelta, timezone
from random import randint
from django.contrib.auth import get_user_model
from django.db.models import Sum
from storeapp.models import Cart
from .models import EarningPoint

User = get_user_model()

class EarningPointsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def reset_earning_points(self, customer):
        current_datetime = datetime.now(timezone.utc)
        current_date = current_datetime.date()

        # Calculate the start and end dates of the current week
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Get the earning points within the current week
        earning_points_within_week = EarningPoint.objects.filter(
            customer_point=customer,
            date__range=[start_of_week, end_of_week]
        )

        # Check if there are earning points within the week
        if earning_points_within_week:
            return  # Skip resetting visit days if earning points exist within the week

        # Reset the visit days to 1 for the current date
        EarningPoint.objects.filter(
            customer_point=customer,
            date=current_date
        ).update(visit_days=1)
        
    def create_or_update_earning_points(self, customer):
        current_datetime = datetime.now(timezone.utc)
        current_date = current_datetime.date()

        # Check if earning points already exist for the current date
        existing_points = EarningPoint.objects.filter(customer_point=customer, date=current_date).exists()
        if existing_points:
            return  # Skip creating new points if already exist for the current date

        # Get the previous earning points for the customer
        previous_points = EarningPoint.objects.filter(customer_point=customer, date=current_date - timedelta(days=1)).first()

        if previous_points:
            # Check if the streak is broken (elapsed time > 24 hours)
            elapsed_time = current_datetime - previous_points.last_visit_datetime
            if elapsed_time > timedelta(days=1):
                # Reset the visit days and points to start a new week
                visit_days = 1
                points = randint(1, 5)
            else:
                # Continue the streak, increment the visit days and points
                visit_days = previous_points.visit_days + 1
                points = min(previous_points.points + randint(5, 15), 10)
        else:
            # Start a new week, set visit days and points to 1
            visit_days = 1
            points = randint(1, 5)

        # Update the points, visit days, and last visit datetime
        EarningPoint.objects.create(
            customer_point=customer,
            date=current_date,
            points=points,
            visit_days=visit_days,
            last_visit_datetime=current_datetime,
            balance=points
        )

    def update_balance(self, customer):
        total_points = EarningPoint.objects.filter(customer_point=customer).aggregate(total_points=Sum('points'))['total_points'] or 0
        balance_cents = total_points * 1
        earning_points = EarningPoint.objects.filter(customer_point=customer, date=datetime.now(timezone.utc).date()).first()

        if earning_points:
            earning_points.balance = balance_cents
            earning_points.save()

    def deduct_expiring_points(self, customer):
        current_date = datetime.now(timezone.utc).date()
        two_months_from_now = current_date + timedelta(days=60)
        expiring_points = EarningPoint.objects.filter(
            customer_point=customer,
            date__gt=current_date,
            date__lte=two_months_from_now
        ).values_list('points', flat=True)
        total_points_to_deduct = sum(expiring_points)

        if total_points_to_deduct > 0:
            earning_points = EarningPoint.objects.filter(customer_point=customer, date=current_date).first()

            if earning_points:
                remaining_points = max(earning_points.points - total_points_to_deduct, 0)
                earning_points.points = remaining_points
                earning_points.balance = remaining_points
                earning_points.save()

    def calculate_total_price(self, cart, points_to_deduct):
        total_price = cart.cart_total - int(points_to_deduct)
        return total_price

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            customer = User.objects.get(pk=request.user.pk)

            self.reset_earning_points(customer)

            if request.path == '/user/earning_points':
                self.create_or_update_earning_points(customer)

            if request.path == '/checkout' and request.method == 'POST':
                cart = Cart.objects.get(session_id=request.session['nonuser'])
                points_to_deduct = request.POST.get('points', 0)
                total_price = self.calculate_total_price(cart, points_to_deduct)
                cart.total_price = total_price
                cart.save()

        return response
