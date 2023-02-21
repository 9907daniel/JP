from django_filters import rest_framework as filters
from .models import Job

class JobsFilter(filters.FilterSet):
    
    min_salary = filters.NumberFilter(field_name="salary" or 0, lookup_expr="gte")
    max_salary = filters.NumberFilter(field_name="salary" or 1000000000, lookup_expr="lte")    
    keyword = filters.CharFilter(field_name="title", lookup_expr='icontains')
    location = filters.CharFilter(field_name="address", lookup_expr='icontains')
    
    
    # filter for education, jobtype and experience
    class Meta: 
        model = Job
        fields = ('education', 'keyword','location','jobType','experience','min_salary','max_salary')