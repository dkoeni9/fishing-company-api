from django.db import models

from users.models import User


class Fish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "api"
        db_table = "fish"
        verbose_name_plural = "fishes"


def fishing_base_photo_path(instance, filename):
    return f"Photos/FishingBases/{instance.id}.jpg"


class FishingBase(models.Model):
    company = models.ForeignKey("api.Company", models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    fish = models.ManyToManyField(
        Fish, through="FishInFishingBase", related_name="fishing_bases"
    )
    photo = models.ImageField(upload_to=fishing_base_photo_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"'{self.name}' fishing base of '{self.company.name}' company"

    class Meta:
        app_label = "api"
        db_table = "fish_base"


class FishInFishingBase(models.Model):
    fishing_base = models.ForeignKey(
        FishingBase, on_delete=models.CASCADE, db_column="fish_base_id"
    )
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    price_per_kilo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = "api"
        db_table = "fish_in_base"
        unique_together = ("fishing_base", "fish")


class FishingBaseStaff(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="fishing_base_staff"
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
