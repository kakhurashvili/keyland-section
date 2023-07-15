from django.contrib import admin
from .models import *
from django.template.response import TemplateResponse

# Register your models here.
from django import forms
from django.contrib import admin
from .models import Category, Main_Category, Sub_Category, Product, Banner,InfoBox,Banner_second
from django.contrib import admin

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subtitle', 'display_image')

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    display_image.short_description = 'Image'
    display_image.admin_order_field = 'image'


admin.site.register(Banner_second)
admin.site.register(InfoBox)

class SubCategoryInline(admin.TabularInline):
    model = Sub_Category
    extra = 0

class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0
    inlines = [SubCategoryInline]

class MainCategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    list_display = ('title', 'status')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'timestamp', 'country')


admin.site.register(Main_Category, MainCategoryAdmin)
admin.site.register(Category)
admin.site.register(Sub_Category)




class ProductAdmin(admin.ModelAdmin):
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'beautiful-description-form'}))
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(SavedItem)

admin.site.register(SiteConfiguration)
from django.contrib import admin
from .models import Cartitems

class CartitemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'subtotal',  'revenue_yesterday')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(subtotal=models.F('quantity') * models.F('product__old_price'))
        return queryset


    def subtotal(self, obj):
        return obj.subtotal

    subtotal.admin_order_field = 'subtotal'



    def revenue_yesterday(self, obj):
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        revenue_yesterday_result = (
            Cartitems.objects
            .filter(cart__created__date=yesterday, cart__owner=obj.cart.owner)
            .annotate(subtotal=models.F('quantity') * models.F('product__old_price'))
            .aggregate(total=models.Sum('subtotal'))
        )
        revenue_yesterday = revenue_yesterday_result['total'] if revenue_yesterday_result['total'] is not None else 0
        return revenue_yesterday

    revenue_yesterday.short_description = 'Revenue Yesterday'

admin.site.register(Cartitems, CartitemsAdmin)

