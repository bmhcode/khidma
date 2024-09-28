import django_filters         # pip install django-filter
from app.models import Post 

class PostFilter(django_filters.FilterSet):
    
    # title = django_filters.CharFilter(lookup_expr='icontains')
    # price = django_filters.RangeFilter()
    
    class Meta:
        model = Post
        # fields = ['category','ville'] # '__all__'
        fields = {
            'title' : ['icontains'], #'istartswith'
            'category': ['exact'],
            'ville' : ['exact'], # ['lt','gt']
        }

     