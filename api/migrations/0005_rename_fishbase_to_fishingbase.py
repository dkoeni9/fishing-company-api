import django.db.models.deletion
import fishing_bases.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_alter_fishingsession_staff"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="FishBase",
            new_name="FishingBase",
        ),
        migrations.RenameModel(
            old_name="FishInBase",
            new_name="FishInFishingBase",
        ),
        migrations.RenameField(
            model_name="fishinfishingbase",
            old_name="fish_base",
            new_name="fishing_base",
        ),
        migrations.RenameField(
            model_name="fishingsession",
            old_name="fish_base",
            new_name="fishing_base",
        ),
        migrations.RenameField(
            model_name="staffprofile",
            old_name="fish_base",
            new_name="fishing_base",
        ),
        migrations.AlterField(
            model_name="fishingbase",
            name="fish",
            field=models.ManyToManyField(
                related_name="fishing_bases",
                through="api.FishInFishingBase",
                to="api.fish",
            ),
        ),
        migrations.AlterField(
            model_name="fishingbase",
            name="photo",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=fishing_bases.models.fishing_base_photo_path,
            ),
        ),
        migrations.AlterField(
            model_name="fishinfishingbase",
            name="fishing_base",
            field=models.ForeignKey(
                db_column="fish_base_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="api.fishingbase",
            ),
        ),
        migrations.AlterField(
            model_name="fishingsession",
            name="fishing_base",
            field=models.ForeignKey(
                db_column="fish_base_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="api.fishingbase",
            ),
        ),
        migrations.AlterField(
            model_name="staffprofile",
            name="fishing_base",
            field=models.ForeignKey(
                blank=True,
                db_column="fish_base_id",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="staff",
                to="api.fishingbase",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="fishinfishingbase",
            unique_together={("fishing_base", "fish")},
        ),
    ]
