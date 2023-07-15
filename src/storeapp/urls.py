from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('product/<str:slug>/<str:sku>/', views.detail, name = 'detail'),
    path('category/', views.category, name='category'),
    path('category/<str:main_category_slug>/', views.category, name='category'),
    path('category/<str:main_category_slug>/<str:category_slug>/', views.category, name='category'),
    path('category/<slug:main_category_slug>/<slug:category_slug>/<slug:sub_category_slug>/', views.category, name='category'),
    path('ajax/product-quick-view/<str:slug>/<str:sku>/', views.product_quick_view, name='product_quick_view'),
    path('chat/', views.chat, name='chat'),

   # path('category/<str:slug>/', views.category, name='category'),
    path('cart', views.cart, name = 'cart'),
    path('updateCart/', views.updateCart, name = 'updateCart'),
    path('updatequantity', views.updateQuantity),
    path('deleteitems', views.deleteCartitems),
    path('checkout', views.checkout, name = 'checkout'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('instagram-photos/', views.get_instagram_photos, name='instagram_photos'),

    path('payment', views.confirmPayment),
    path('saveditems', views.saveItems, name = 'saveitems'),
    path('addsaveitems', views.addSavedItems),
    path('order', views.order, name = 'order'),
    path('account', views.account, name = 'account'),
    path('updateaccount', views.update_user_info, name = 'updateaccount'),
    path('search', views.search, name = 'search'),



]