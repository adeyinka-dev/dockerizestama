# Generated by Django 4.2.3 on 2023-08-13 12:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_tenant_rent_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tenant",
            name="rent_start_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]