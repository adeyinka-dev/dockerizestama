# Generated by Django 4.2.3 on 2023-09-06 17:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0017_managerproxy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tenant",
            name="phone_number",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
