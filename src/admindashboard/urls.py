from django.urls import path
from . import views
from .views import UserProfileView 


urlpatterns = [
        path('', views.index, name = 'admin_dashboard'),
        path('user-card/', UserProfileView.as_view(), name='user-card'),
        path('user-list/delete-customer/<int:customer_id>/', UserProfileView.delete_customer, name='delete-customer'),

        path('user-list/', UserProfileView.user_list, name='user-list'),
        path('user-profile/', UserProfileView.user_profile, name='user-profile'),
        path('search-customers/', views.search_customers, name='search-customers'),

]



