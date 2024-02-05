from django.http import JsonResponse
from django.test import RequestFactory, TestCase

from core.exceptions.base import CustomError
from core.middlewares.exception_interceptor import ExceptionInterceptorMiddleware


class ExceptionInterceptorMiddlewareTestCase(TestCase):
    def setUp(self):
        self.middleware = ExceptionInterceptorMiddleware(get_response=None)
        self.factory = RequestFactory()

    def test_process_exception(self):
        request = self.factory.get("/")
        exception = CustomError(error_code=123, error_message="Custom error message")
        response = self.middleware.process_exception(request, exception)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"),
            '{"error": "Custom error message", "code": 123}',
        )

    def test_process_exception_handles_non_custom_error(self):
        request = self.factory.get("/")
        exception = ValueError("Some error message")
        response = self.middleware.process_exception(request, exception)

        self.assertIsNone(response)
