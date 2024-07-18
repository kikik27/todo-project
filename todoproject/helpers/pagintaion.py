from math import ceil

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Paginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 9000
    page_query_param = 'page'

    def get_paginated_response(self, data, message_param=None, **kwargs):
        total_items = self.page.paginator.count
        current_page_size = self.get_page_size(self.request)
        total_pages = ceil(total_items / current_page_size)

        message = message_param if message_param is not None else "Success"

        return Response({
            'status': 200,
            'message': message,
            'data': data,
            **kwargs,
            'meta': {
                'paginator': {
                    'next': self.get_next_link(),
                    'prev': self.get_previous_link(),
                    'page_size': current_page_size,
                    'count': total_items,
                    'pages': total_pages,
                    'current_page': self.page.number,
                }
            }
        })
