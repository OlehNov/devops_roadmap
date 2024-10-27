import os
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomListViewPageNumberPagination(PageNumberPagination):

    def get_page_size(self, request):
        page_size = request.query_params.get("page_size", self.page_size)
        max_page_size = os.getenv("MAX_PAGE_SIZE")
        return min(int(page_size), max_page_size)

    def get_paginated_response(self, data):
        return Response({
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link()
            },
            "total": self.page.paginator.count,
            "page": self.page.number,
            "page_size": self.get_page_size(self.request),
            "results": data
        })
