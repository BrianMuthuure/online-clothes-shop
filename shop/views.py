from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic.base import View

from shop.models import Item, OrderItem, Order


def home(request):
    return render(request, 'home.html')


class ItemListView(ListView):
    model = Item
    template_name = 'shop/item_list.html'
    context_object_name = 'items'
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        context = super(ItemListView, self).get_context_data(*args, **kwargs)
        return context


def item_detail(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug, available=True)
    context = {
        'item': item,
    }
    return render(request, 'shop/item_detail.html', context)


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, 'Item quantity was updated successfully')
            return redirect('shop:order-summary')
        else:
            messages.success(request, 'This item was added to your cart')
            order.items.add(order_item)
    else:
        date_ordered = timezone.now()
        order = Order.objects.create(user=request.user, date_ordered=date_ordered)
        order.items.add(order_item)
    return redirect('shop:order-summary')


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.warning(request, "This item was removed from cart")
        else:
            messages.error(request, 'This item was not in your cart')
            return redirect("shop:order-summary")
    else:
        messages.error(request, 'You do not have an active order')
        return redirect("shop:order-summary")
    return redirect("shop:order-summary")


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order/order_detail.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")


def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.item = None
            messages.success(request, 'This item quantity was updated')
            return redirect("shop:order-summary")
        else:
            messages.error(request, 'This item was not in your cart')
            return redirect("shop:order-summary")
    else:
        messages.error(request, "You do not have an active order")
        return redirect("shop:order-summary")