from django_filters import rest_framework as filters
from .models import Client
from django.db import models


class ClientFilter(filters.FilterSet):
    # name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    search = filters.CharFilter(method='search_filter')

    class Meta:
        model = Client
        fields = ['search']

    def search_filter(self, queryset, name, value):
        return queryset.filter(models.Q(first_name__icontains=value) | models.Q(last_name__icontains=value) |
                               models.Q(sure_name__icontains=value) | models.Q(phone__icontains=value))


class ApartmentFilter(filters.FilterSet):

    pass