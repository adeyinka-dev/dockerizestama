# Generated by Django 4.2.3 on 2023-08-27 21:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0015_alter_tenant_user_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tenant",
            name="matric_num",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
