from django.urls import path

from shop.views import home, item_detail, ItemListView, add_to_cart, OrderSummaryView, remove_from_cart, \
    remove_single_item_from_cart

app_name = 'shop'

urlpatterns = [
    path('', home, name='home'),
    path('items/', ItemListView.as_view(), name='item_list'),
    path('<int:id>/<slug:slug>/', item_detail, name='item_detail'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),

    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart'),

    path('remove-item-from-cart/<slug:slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
]