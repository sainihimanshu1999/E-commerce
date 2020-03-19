from django.conf import settings
from django.db import models

# list of item displayed


class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.title

# intermediate step


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

# ordered items just like an shoping cart


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
