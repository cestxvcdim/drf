from rest_framework.pagination import PageNumberPagination


class LessonPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        queryset = queryset.order_by('id')
        return super().paginate_queryset(queryset, request, view)


class CoursePaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        queryset = queryset.order_by('id')
        return super().paginate_queryset(queryset, request, view)
