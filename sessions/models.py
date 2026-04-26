from django.db import models

from fishing_bases.models import FishingBase
from users.models import User


class FishingSession(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 1, "Created"
        STARTED = 2, "Started"
        CLOSED = 3, "Closed"

    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.CREATED
    )
    fishing_base = models.ForeignKey(
        FishingBase, on_delete=models.CASCADE, db_column="fish_base_id"
    )
    staff = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="sessions", null=True
    )
    fisher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    number_of_people = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Fishing session at {self.fishing_base.name} by {self.staff.username}"

    class Meta:
        app_label = "api"
        db_table = "fishing_session"
