
from django.db import models
from django.utils.timezone import now
from uuid import uuid4


class Chapter(models.Model):
    STATUS_CHOICES = (
        ("disponible", "Disponible"),
        ("reservado", "Reservado"),
        ("alquilado", "Alquilado"),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    season = models.IntegerField()
    episode = models.IntegerField()
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="disponible"
    )
    reserved_at = models.DateTimeField(null=True, blank=True)
    rented_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"S{self.season}E{self.episode} - {self.title} ({self.status})"
