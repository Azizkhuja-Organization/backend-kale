# Generated by Django 4.2.3 on 2023-08-28 10:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("banner", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="banner",
            old_name="link",
            new_name="url",
        ),
        migrations.RenameField(
            model_name="smallbanner",
            old_name="link",
            new_name="url",
        ),
    ]
