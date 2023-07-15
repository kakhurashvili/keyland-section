from email.policy import default
from django.db import models
import uuid
from django.contrib.auth.models import User
from  django.conf import settings
from UserProfile.models import Customer
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random
import string
from django.core.validators import MinLengthValidator
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
from django.db.models import F, Sum
from decimal import Decimal
from colorfield.fields import ColorField
from django.utils.html import format_html

# Create your models here.

class SiteConfiguration(models.Model):
    logo = models.ImageField(upload_to='logo/')
    # Add other fields if needed

    def __str__(self):
        return "Site Configuration"


        

class Main_Category(models.Model):
    STATUS = (
        ('True','True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    slug = models.SlugField(default= None)
    status = models.CharField(max_length=10, choices=STATUS)
    featured_product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='featured_product')
    icon = models.CharField(max_length=100, default=None, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', args=[self.slug, ''])

class Category(models.Model):
    main_category = models.ForeignKey(Main_Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(default= None)

    def __str__(self):
        return self.title + " -- " + self.main_category.title

    def get_absolute_url(self):
        return reverse('category', args=[self.main_category.slug, self.slug])

class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(default= None)

    def __str__(self):
        return self.category.main_category.title + " -- " + self.category.title + " -- " + self.title

    def get_absolute_url(self):
        return reverse('category', args=[self.category.main_category.slug, self.category.slug, self.slug])


  
def generate_sku():
    while True:
        unique_id = str(uuid.uuid4().int)[:7]  # Get the first 7 characters of a UUID integer
        sku = f"800{unique_id.zfill(8)}"  # Prepend "800" and zero-pad the remaining characters to a total length of 11
        if not Product.objects.filter(sku=sku).exists():
            return sku
        
  
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)
    discount = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    image = models.ImageField(upload_to='img', blank=True, null=True, default='')
    old_price = models.FloatField(default=100.00)
    sub_category = models.ForeignKey(Sub_Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    slug = models.SlugField(default=None)
    sku = models.CharField(max_length=11, unique=True, validators=[MinLengthValidator(11)], default=generate_sku)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    inventory = models.IntegerField(default=5)
    top_deal = models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)

    @property
    def price(self):
        if self.discount and self.discount_percentage:
            discount_percentage = Decimal(self.discount_percentage)
            new_price = Decimal(self.old_price) - ((discount_percentage / 100) * Decimal(self.old_price))
        else:
            new_price = Decimal(self.old_price)
        return new_price

    @property
    def img(self):
        if self.image == "":
            self.image = ""
        return self.image

    def __str__(self):
        return self.name 
    
@receiver(pre_save, sender=Product)
def update_discount_percentage(sender, instance, **kwargs):
    if not instance.discount:
        instance.discount_percentage = 0

class Cart(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
    cart_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100)
    unipay_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    unipay_payment_status = models.CharField(max_length=50, blank=True, null=True)

    

    @property
    def num_of_items(self):
        cartitems = self.cartitems_set.all()
        qtysum = sum([ qty.quantity for qty in cartitems])
        return qtysum
    
    @property
    def cart_total(self):
        cartitems = self.cartitems_set.all()
        qtysum = sum([ qty.subTotal for qty in cartitems])
        return qtysum
    

    
    def __str__(self):
        return str(self.cart_id)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.IntegerField(default=0)
    
    @property
    def subTotal(self):
        total = self.quantity * self.product.price
        
        return total
    


class SavedItem(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    added = models.IntegerField(default=0)
    
    
    
    def __str__(self):
        return str(self.id)
    

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100,null=True, blank=True )

    def __str__(self):
        return self.ip_address
    


class Banner(models.Model):
    HEIGHTS = (
        ('x1', 'Height 1'),
        ('x2', 'Height 2'),
        ('x3', 'Height 3'),
    )


    size_value = models.PositiveIntegerField()
    height = models.CharField(max_length=10, choices=HEIGHTS)
    image_width = models.PositiveIntegerField()
    image_height = models.PositiveIntegerField()

    image = models.ImageField(upload_to='banners/')
    title = models.CharField(max_length=100, blank=True, default='')
    subtitle = models.CharField(max_length=100, blank=True, default='')

    button_text = models.CharField(max_length=100,blank=True,null=True)
    button_link = models.URLField(null=True, blank=True)
    color = ColorField(default='#000000')

    def __str__(self):
        id_str = str(self.id) if self.id else "N/A"
        return f"ID: {id_str} | Title: {self.title} | Subtitle: {self.subtitle}"

class Banner_second(models.Model):
    font1 = models.CharField(max_length=100)
    heading = models.CharField(max_length=100)
    button_text = models.CharField(max_length=100)
    button_link = models.CharField(max_length=200)
    coupon_text = models.CharField(max_length=100)
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.heading
    
class InfoBox(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.title