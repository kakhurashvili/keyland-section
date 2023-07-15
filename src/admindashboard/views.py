from datetime import date, datetime, timedelta
from django.forms import DecimalField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.utils import timezone
from admindashboard.models import UserActivityData
from core.models import User
from storeapp.models import Cart, Cartitems, Product
from UserProfile.models import Customer, EarningPoint
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from decimal import Decimal
import json
from django.views import View



def update_user_activity_data():
    now = timezone.now()
    start_date = now.date() - timedelta(days=1)
    end_date = now.date()
    
    active_users = get_user_model().objects.filter(last_login__date__range=(start_date, end_date))
    inactive_users = get_user_model().objects.exclude(last_login__date__range=(start_date, end_date))

    # Update the user activity data in the database
    activity_data, _ = UserActivityData.objects.get_or_create(date_label=start_date.strftime("%d %b"))
    activity_data.active_users = active_users.count()
    activity_data.inactive_users = inactive_users.count()
    
    activity_data.save()

def get_user_activity_data(start_date=None, end_date=None):
    if not start_date or not end_date:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=3)

    activity_data = []

    current_date = start_date
    while current_date <= end_date:
        active_users = User.objects.filter(last_login__date=current_date).count()
        inactive_users = User.objects.exclude(last_login__date=current_date).count()

        activity_data.append({
            "active_users": active_users,
            "inactive_users": inactive_users,
            "date_label": current_date.strftime("%d %b"),
        })

        current_date += timedelta(days=1)

    return activity_data



def index(request):
    User = get_user_model()
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    now = timezone.now()

    signups_today = User.objects.filter(date_joined__date=today).count()
    signups_yesterday = User.objects.filter(date_joined__date=yesterday).count()

    visitors_today = User.objects.filter(last_login__date=today).count()
    visitors_yesterday = User.objects.filter(last_login__date=yesterday).count()

    users_today = User.objects.filter(date_joined__date=today)
    user_emails_today = [user.email for user in users_today]

    orders_today = Cart.objects.filter(created__date=today, completed=True).count()
    print('orders_today',orders_today)
    today = date.today()
    from django.db.models import Sum, F, FloatField, ExpressionWrapper

    revenue_today = Cartitems.objects.filter(
        cart__created__date=today, cart__completed=True
    ).annotate(
        subtotal=ExpressionWrapper(
            F("quantity") * (
                F("product__old_price") - (
                    F("product__old_price") * F("product__discount_percentage") / 100
                )
            ),
            output_field=FloatField()
        )
    ).aggregate(
        total=Sum("subtotal", output_field=FloatField())
    )["total"] or 0

    print(f"Revenue for today: {revenue_today}")

    timestamps = []
    for i in range(11):
        minutes = (i + 1) * 10
        if minutes >= 60:
            hours = minutes // 60
            minutes %= 60
            label = f"{hours}h"
            if minutes > 0:
                label += f" {minutes}m"
        else:
            label = f"{minutes}m"
        timestamps.append(label)

    signup_counts = []
    for i in range(11):
        start_minutes = i * 10
        end_minutes = (i + 1) * 10
        signup_count = User.objects.filter(date_joined__range=(now - timedelta(minutes=end_minutes), now - timedelta(minutes=start_minutes))).count()
        signup_counts.append(signup_count)

    chart_data = {
        "labels": timestamps,
        "data": signup_counts,
    }

    chart_data_json = json.dumps(chart_data)

    sales_data = Cartitems.objects.filter(cart__completed=True)
    
    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Decimal):
                return float(obj)
            return super().default(obj)

    acqData = []
    for item in sales_data:
        acqData.append({
            "first": [float(item.quantity)],
            "second": [str(item.product.price)],
        })

    acqData_json = json.dumps(acqData, cls=DecimalEncoder)

    # Update the user activity data
    update_user_activity_data()

  

  
    # Get the start_date and end_date values from the HTML form or request data
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    # Convert start_date and end_date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

    print('start_date:', start_date, 'end_date:', end_date)

    # Get the user activity data based on the provided start_date and end_date
    activity_data = get_user_activity_data(start_date=start_date, end_date=end_date)

    # Convert the activity_data to JSON format
    try:
        activityData_json = json.dumps(activity_data)
    except Exception as e:
        print("Error converting activity_data to JSON:", str(e))
        activityData_json = None
    print('activityData_json', activityData_json)

    
    from django.db.models import Sum

    sold_items = Cartitems.objects.filter(
        cart__completed=True
    ).values(
        'product__name'
    ).annotate(
        total_quantity_sold=Sum('quantity')
    ).order_by('product__name')

    cart_total_quantity = Cartitems.objects.filter(
        cart__completed=True
    ).aggregate(
        total_quantity=Sum('quantity')
    )['total_quantity']

    for item in sold_items:
        percentage_sold = (item['total_quantity_sold'] / cart_total_quantity) * 100
        item['percentage_sold'] = round(percentage_sold, 2)

    print('sold_items',sold_items)
    top_deals = Product.objects.filter(top_deal=True)
    print('top_deals',top_deals)

    # Retrieve total point balances for all users
    # Retrieve total balance for all users
    total_balance = EarningPoint.objects.aggregate(total_balance=Sum('balance')).get('total_balance')
    balance_dollars = Decimal(total_balance / 100) if total_balance is not None else Decimal(0)
    print("balance_dollars",balance_dollars)


    context = {
        "signups_today": signups_today,
        "signups_yesterday": signups_yesterday,
        "visitors_today": visitors_today,
        "visitors_yesterday": visitors_yesterday,
        "user_emails_today": user_emails_today,
        "balance_dollars":balance_dollars,
        "orders_today": orders_today,
        "sold_items": sold_items,
        "revenue_today": revenue_today,
        "acqData_json": acqData_json,
        "activityData_json": activityData_json,
        "chart_data_json": chart_data_json,
        "top_deals": top_deals,

    }

    return render(request, "dashboard/index.html", context)




class UserProfileView(View):
    def get(self, request):
        return render(request, 'dashboard/user-card.html')

    def user_list(request):
        customers = Customer.objects.all()  # Retrieve all customers from the database
        
        context = {
            'customers': customers
        }
        return render(request, 'dashboard/user-list.html', context)

    def user_profile(request):
        return render(request, 'dashboard/user-profile.html')
    

    def delete_customer(request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        
        # Delete the associated user
        user = customer.user
        user.delete()
        
        # Delete the customer
        customer.delete()
        
        return redirect('user-list')
    
    
def search_customers(request):
    query = request.GET.get('query')
    customers = Customer.objects.filter(name__icontains=query)
    context = {
        'customers': customers
    }
    return render(request, 'dashboard/search-results.html', context)
