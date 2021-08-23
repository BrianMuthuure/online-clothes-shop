from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from shop.managers import ItemManager


class Item(models.Model):
    CATEGORIES = (
        ('Men', 'Men'),
        ('Ladies', 'Ladies')
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, db_index=True)
    category = models.CharField(choices=CATEGORIES, max_length=10)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField(default=timezone.now)

    objects = ItemManager()

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('shop:item_detail', args=[self.id, self.slug])

    def get_add_to_cart_url(self):
        return reverse('shop:add-to-cart', args=[self.slug])


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} ({self.item}) "

    def get_total_item_price(self):
        return self.quantity*self.item.price

    def get_total_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.id}'

    def get_order_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total
