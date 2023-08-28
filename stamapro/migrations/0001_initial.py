# Generated by Django 4.2.3 on 2023-08-28 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hostel_name", models.CharField(max_length=200)),
                ("address", models.TextField()),
                ("number_of_rooms", models.PositiveIntegerField()),
                ("additional_features", models.TextField(blank=True)),
                ("contact_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(blank=True, max_length=15, null=True)),
                ("date_submitted", models.DateTimeField(auto_now_add=True)),
                (
                    "service_status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("contacted", "Contacted"),
                            ("accepted", "Accepted"),
                            ("verified", "Verified"),
                            ("approved", "Approved"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
