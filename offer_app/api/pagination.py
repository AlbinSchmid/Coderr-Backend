from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    """
    Custom pagination class for large result sets.
    """
    page_size = 105
    page_size_query_param = 'page_size'
    max_page_size = 10000