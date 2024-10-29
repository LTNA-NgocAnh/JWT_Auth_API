from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Session


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data["refresh"]
        user = request.user
        Session.objects.create(user=user, refresh_token=refresh_token)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get("refresh")
        access_token = response.data.get("access")
        user = request.user

        session, created = Session.objects.update_or_create(
            user=user,
            refresh_token=refresh_token,
            defaults={"last_used_at": timezone.now()},
        )

        if not created:
            Session.objects.filter(user=user).exclude(
                refresh_token=refresh_token
            ).delete()

        return response


import logging

logger = logging.getLogger("django.request")


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        logger.info(f"User  {request.data['username']} is requesting tokens.")
        response = super().post(request, *args, **kwargs)
        return response


def revoke_tokens(user):
    Session.objects.filter(user=user).delete()  # Remove all sessions for the user


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.session_set.all().delete()  # Log out from all devices
        return Response({"detail": "Logged out successfully."})


class RevokeTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Session.objects.filter(user=request.user).delete()
        return Response({"detail": "Tokens revoked successfully."})


def detect_abnormal_usage(user):
    sessions = Session.objects.filter(user=user)
    if sessions.count() > 5:  # Example threshold
        revoke_tokens(user)  # Revoke tokens if abnormal usage is detected
