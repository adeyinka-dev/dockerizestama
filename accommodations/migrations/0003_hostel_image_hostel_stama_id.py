# Generated by Django 4.2.3 on 2023-07-16 14:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accommodations", "0002_alter_hostel_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="hostel",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="hostels"),
        ),
        migrations.AddField(
            model_name="hostel",
            name="stama_id",
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
