from django.db import connection
import logging 

logger = logging.getLogger(__name__)

class QueryCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        query_count = len(connection.queries)
        logger.debug(f'{query_count} queries made in {request}')
        return response