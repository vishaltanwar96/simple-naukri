from django_filters import rest_framework as filters

from core.models import Job


class JobFilterSet(filters.FilterSet):

    recruiter_fname = filters.CharFilter(field_name='posted_by', lookup_expr='first_name__iexact')
    recruiter_lname = filters.CharFilter(field_name='posted_by', lookup_expr='last_name__iexact')

    class Meta:
        model = Job
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
        }
