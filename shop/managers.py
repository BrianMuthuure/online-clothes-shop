from django.db import models
from django.db.models import Q


class ItemQuerySet(models.query.QuerySet):
    def available(self):
        return self.filter(available=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query) |
            Q(category__icontains=query)
        )
        return self.filter(lookups).distinct()


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self.db)

    def all(self):
        return self.get_queryset().available()

    def search(self, query):
        return self.get_queryset().search(query)