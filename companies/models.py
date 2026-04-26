from django.db import models

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
