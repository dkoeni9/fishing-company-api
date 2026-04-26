from django.db import models


class Fish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "api"
        db_table = "fish"
        verbose_name_plural = "fishes"


def fishbase_photo_path(instance, filename):
    return f"Photos/FishBases/{instance.id}.jpg"


class FishBase(models.Model):
    company = models.ForeignKey("api.Company", models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    fish = models.ManyToManyField(Fish, through="FishInBase", related_name="bases")
    photo = models.ImageField(upload_to=fishbase_photo_path, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"'{self.name}' base of '{self.company.name}' company"

    class Meta:
        app_label = "api"
        db_table = "fish_base"


class FishInBase(models.Model):
    fish_base = models.ForeignKey(FishBase, on_delete=models.CASCADE)
    fish = models.ForeignKey(Fish, on_delete=models.CASCADE)
    price_per_kilo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = "api"
        db_table = "fish_in_base"
        unique_together = ("fish_base", "fish")
