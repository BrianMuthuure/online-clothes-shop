from django.urls import path

from search.views import ItemSearchView

urlpatterns = [
    path('', ItemSearchView.as_view(), name='query'),
]