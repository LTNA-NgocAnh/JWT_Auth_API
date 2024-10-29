from django.db import models
from django.contrib.auth import get_user_model


class Session(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(auto_now=True)
