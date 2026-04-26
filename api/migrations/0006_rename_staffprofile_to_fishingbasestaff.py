import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0005_rename_fishbase_to_fishingbase"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="StaffProfile",
            new_name="FishingBaseStaff",
        ),
        migrations.AlterModelTable(
            name="fishingbasestaff",
            table="staff_profile",
        ),
        migrations.AlterField(
            model_name="fishingbasestaff",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fishing_base_staff",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
