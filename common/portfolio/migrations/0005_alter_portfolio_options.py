# Generated by Django 4.2.3 on 2023-08-18 07:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0004_alter_portfolioimage_photo"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="portfolio",
            options={"ordering": ["-id"]},
        ),
    ]
