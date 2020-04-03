from django.urls import path
from .views import HomeView
from .views import checkout
from .views import ItemDetailView
from .views import add_to_cart
from .views import remove_from_cart

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view() , name = 'home'),
    path('checkout/', checkout , name = 'checkout'),
    path('products/<slug>/', ItemDetailView.as_view(), name = 'products'),
    path('add-to-cart/<slug>/', add_to_cart, name = 'add-to-cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name = 'remove-from-cart'),
    


]