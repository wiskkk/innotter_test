from django_filters.rest_framework import FilterSet, filters

from mainapp.models import Page


class PageFilterSet(FilterSet):
    tags = filters.CharFilter(distinct=True, method='filter_tags')

    class Meta:
        model = Page
        fields = ['tags']

    def filter_tags(self, queryset, name, value):
        for page in queryset:
            for tag in page.tags.all():
                if tag.name == value:
                    return queryset.filter(tags=tag.id)
