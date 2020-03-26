from django.urls import path
from .views import HomeView
from .views import checkout
from .views import products

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view() , name = "home"),
    path('checkout/', checkout , name = "checkout"),
    path('products/', products, name = "products"),
    


]