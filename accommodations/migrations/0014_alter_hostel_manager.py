# Generated by Django 4.2.3 on 2023-08-30 20:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accommodations", "0013_alter_hostel_manager"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hostel",
            name="manager",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="management",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
