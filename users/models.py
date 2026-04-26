from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Value
from django.db.models.functions import Now
from django.utils import timezone


class User(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False, db_default=Value(False))
    is_staff = models.BooleanField(default=False, db_default=Value(False))
    is_active = models.BooleanField(default=True, db_default=Value(True))
    date_joined = models.DateTimeField(default=timezone.now, db_default=Now())
    last_login = models.DateTimeField(blank=True, null=True)

    REQUIRED_FIELDS = ["first_name", "middle_name", "last_name"]

    def __str__(self):
        return self.username

    class Meta:
        app_label = "api"
        db_table = "user"
