# Generated by Django 4.2.3 on 2023-08-18 07:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("partner", "0002_partner_description_en_partner_description_ru_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="partner",
            options={"ordering": ["-id"]},
        ),
    ]
