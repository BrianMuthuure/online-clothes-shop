from django.contrib import admin
from .models import Item, OrderItem, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'available', 'date_created', 'date_updated']
    list_filter = ['available', 'date_created', 'date_updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(OrderItem)
admin.site.register(Order)