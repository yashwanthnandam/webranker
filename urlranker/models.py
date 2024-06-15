# models.py
from django.db import models

class URLResult(models.Model):
    url = models.URLField(unique=True)
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
