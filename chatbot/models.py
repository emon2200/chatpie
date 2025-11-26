from django.db import models
import uuid

class Tenant(models.Model):
    name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    db_url = models.URLField(blank=True, null=True)
    rest_api = models.JSONField(default=list, blank=True)  # একাধিক URL রাখতে পারবে

    def __str__(self):
        return self.name
