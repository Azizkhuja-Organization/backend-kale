# Generated by Django 4.2.3 on 2023-08-17 17:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_username"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="district",
        ),
        migrations.RemoveField(
            model_name="user",
            name="region",
        ),
        migrations.RemoveField(
            model_name="user",
            name="street",
        ),
    ]
