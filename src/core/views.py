from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.shortcuts import redirect
from .forms import CheckoutForm
from .models import Item, OrderItem, Order, BillingAddress, Payment

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = "products.html"


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data('street_address')
                apartment_address = form.cleaned_data('apartment_address')
                country = form.cleaned_data('country')
                zip = form.cleaned_data('zip')
                same_shipping_address = form.cleaned_data(
                    'same_shipping_address')
                save_info = form.cleaned_data('save_info')
                payment_option = form.cleaned_data('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip

            )
            billing_addresss.save()
            order.billing_address = billing_address
            order.save()
            print("The form is valid")
            return redirect('core:checkout')
            messages.warning(self.request, "Failed Checkout")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        return render(self.request, "payment.html")
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        stripe.Charge.create(
            amount=amount,
            currency="inr",
            source= token, 
        )

        try:
            charge = stripe.Charge.create(
            amount=amount,
            currency="inr",
            source= token, 
            )
            # creating the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = amount
            payment.save() 


            # assigning the payment

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "your order was successful!")
            return redirect("/")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error' , {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit Error")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid Parameters")
            return redirect("/")     
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Authentication error")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Connection failed")
            return redirect("/")   
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong, You were not charged")
            return redirect("/")
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.error(self.request, "Serious Error occured, we have been notified.")
            return redirect("/")      

        




    

                

            

       

        

        





     




@login_required
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
            return redirect("core:order-summary")
        else:
            messages.info(request, "This was added to your cart.")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This was added to your cart.")
        return redirect("core:order-summary")


@login_required
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
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item does not exist in cart.")
            return redirect("core:order-summary")
    else:
        messages.info(request, "You haven't ordered yet.")
        return redirect("core:products", slug=slug)





@login_required
def remove_single_item_from_cart(request, slug):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
           
            messages.info(request, "This item is updated in your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item does not exist in cart.")
            return redirect("core:products", slug=slug)
    else:
        messages.info(request, "You haven't ordered yet.")
        return redirect("core:products", slug=slug)
