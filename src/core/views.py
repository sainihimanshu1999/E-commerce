from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item



class HomeView(ListView):
    model = Item
    template_name = "home.html"





def checkout(request):
    context = {
        'items' : Item.objects.all()
    }
    return render(request, "checkout.html", context )



def products(request):
    context = {
        'items' : Item.objects.all()
    }
    return render(request, "products.html" , context)









