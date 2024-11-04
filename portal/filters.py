from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter, CharFilter

from .models import Post


class NewsFilter(FilterSet):
    header = CharFilter(lookup_expr='icontains', label='Заголовок: ')
    date_after = DateTimeFilter(
        field_name='time_in',
        lookup_expr='gt',
        label='Публикация после: ',
        widget=DateTimeInput(
        format='%Y-%m-%dT%H:%M',
        attrs={'type': 'datetime-local'}
        ),
    )

    class Meta:
        model = Post
        fields = {
            'post_category': ['exact'],
        }
