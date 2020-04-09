from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.shortcuts import redirect
from .models import Item, OrderItem, Order


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        return render(self.request,'order_summary.html' )
    


class ItemDetailView(DetailView):
    model = Item
    template_name = "products.html"


def checkout(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "checkout.html", context)


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # checking wheter the ordern item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity is updated.")
            return redirect("core:products", slug=slug)
        else:
            messages.info(request, "This was added to your cart.")
            order.items.add(order_item)
            return redirect("core:products", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This was added to your cart.")
        return redirect("core:products", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # checking wheter the ordern item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This was removed from your cart.")
            return redirect("core:products", slug=slug)
        else:
            messages.info(request, "This item does not exist in cart.")
            return redirect("core:products", slug=slug)
    else:
        messages.info(request, "You haven't ordered yet.")
        return redirect("core:products", slug=slug)

