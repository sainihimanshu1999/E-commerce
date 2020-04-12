from django.urls import path
from .views import HomeView
from .views import OrderSummaryView
from .views import CheckoutView
from .views import ItemDetailView
from .views import add_to_cart
from .views import remove_from_cart
from .views import remove_single_item_from_cart
from .views import PaymentView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view() , name = 'home'),
    path('checkout/', CheckoutView.as_view() , name = 'checkout'),
    path('order-summary/', OrderSummaryView.as_view() , name = 'order-summary'),
    path('products/<slug>/', ItemDetailView.as_view(), name = 'products'),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name = 'remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name = 'remove-single-item-from-cart'),
    path('payment/<payment_option>', PaymentView.as_view(), name='payment')
    


]