# Generated by Django 4.2.3 on 2023-09-07 05:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0008_alter_catalog_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="catalog",
            name="file",
            field=models.FileField(blank=True, null=True, upload_to="catalogFiles"),
        ),
        migrations.DeleteModel(
            name="CatalogImage",
        ),
    ]
