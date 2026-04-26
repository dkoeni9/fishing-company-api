from django.db import models

from fishing_bases.models import FishingBase
from users.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company",
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = "api"
        db_table = "company"
        verbose_name_plural = "companies"


class StaffProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="staff_profile"
    )
    fishing_base = models.ForeignKey(
        FishingBase,
        on_delete=models.CASCADE,
        related_name="staff",
        blank=True,
        null=True,
        db_column="fish_base_id",
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.fishing_base.name}"

    class Meta:
        app_label = "api"
        db_table = "staff_profile"
