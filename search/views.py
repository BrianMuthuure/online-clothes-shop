from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from shop.models import Item


class ItemSearchView(ListView):
    context_object_name = 'items'
    template_name = 'search/item_search.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ItemSearchView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        print(query)
        if query is not None:
            return Item.objects.search(query)
        return Item.objects.all()
