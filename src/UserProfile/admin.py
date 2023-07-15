from django.contrib import admin
from .models import Address,EarningPoint
from django.db.models import Sum


@admin.register(EarningPoint)
class EarningPointAdmin(admin.ModelAdmin):
    list_display = ('customer_point', 'get_customer_name', 'last_visit_datetime', 'points', 'balance')  # Add 'balance' to the list display

    def get_customer_name(self, obj):
        return f"{obj.customer_point.first_name} {obj.customer_point.last_name}"
    get_customer_name.short_description = 'Customer Name'
    get_customer_name.admin_order_field = 'customer_point__first_name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('customer_point')
        return queryset

    def balance(self, obj):
        return obj.balance
    balance.short_description = 'Balance'

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        total_balance = EarningPoint.objects.aggregate(total_balance=Sum('balance'))['total_balance']
        extra_context['total_balance'] = total_balance or 0  # Handling None value
        return super().changelist_view(request, extra_context=extra_context)


# Register your models here.
admin.site.register(Address)
