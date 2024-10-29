from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView
from .views import LogoutView, RevokeTokenView

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/revoke/", RevokeTokenView.as_view(), name="token_revoke"),
]
