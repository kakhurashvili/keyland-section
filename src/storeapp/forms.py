from django import forms
from django.forms import ModelForm
from UserProfile.models import Address
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from UserProfile.models import Customer
from ckeditor.widgets import CKEditorWidget
from .models import Product

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Product
        fields = '__all__'


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['home_address', 'bus_stop', 'city', 'state']


class UpdateUserForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email']
