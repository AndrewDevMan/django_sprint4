from django.db.models import Count
from django.utils import timezone

from .models import Post


def get_queryset_all_post():
    '''All posts'''
    queryset = Post.objects.select_related(
        'category',
        'location',
        'author',
    ).order_by(
        '-pub_date',
    ).annotate(
        comment_count=Count('comments'),
    )
    return queryset


def get_queryset_published_post():
    '''Published posts'''
    queryset = get_queryset_all_post().filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )
    return queryset
