from django.urls import path
from .views import HomeView
from .views import checkout
from .views import product

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view() , name = "home"),
    path('checkout/', checkout , name = "checkout"),
    path('products.html', product , name = "product"),
    


]