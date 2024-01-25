from django.http import JsonResponse

from core.exceptions.base import CustomError


class ExceptionInterceptorMiddleware:
    """
    Middleware to handle custom exceptions and return structured JSON responses.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """
        Handle custom exceptions and format them into JSON responses.
        """
        if isinstance(exception, CustomError):
            error_response = {
                "error": str(exception),
                "code": exception.error_code,
            }
            return JsonResponse(error_response, status=400)
        return None
