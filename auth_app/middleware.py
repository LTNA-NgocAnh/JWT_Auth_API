from rest_framework.response import Response
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .views import detect_abnormal_usage


class JWTValidationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION", None)
        if auth:
            try:
                token = auth.split()[1]
                JWTAuthentication().get_validated_token(token)
                user = JWTAuthentication().get_user(token)
                detect_abnormal_usage(user)
            except TokenError:
                return Response({"detail": "Invalid token"}, status=401)
