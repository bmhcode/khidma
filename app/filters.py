import django_filters         # pip install django-filter
from app.models import Post 
from django import forms
# from crispy_forms.helper import FormHelper # pip install helper
# from crispy_forms.layout import Layout, Submit, Row, Column
# pip3 install --user django-crispy-forms
from django_filters import DateFilter, CharFilter
  
class PostFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name="posted_at",lookup_expr='gte')
    # end_date = DateFilter(field_name="posted_at",lookup_expr='lte')
    # # note = CharFilter(field_name='note', lookup_expr='icontains')
    class Meta:
        model = Post #   
        fields = { # fields = '__all__  exclude = ['posted_at','is_active',...]
            'title' : ['icontains'], #'istartswith'
            'category': ['exact'],
            'ville' : ['exact'], # ['lt','gt']
            # 'note' : ['icontains'],
            
        }
       
