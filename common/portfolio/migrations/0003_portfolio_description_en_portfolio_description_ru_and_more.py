# Generated by Django 4.2.3 on 2023-08-06 12:57

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0002_portfolio_file3d"),
    ]

    operations = [
        migrations.AddField(
            model_name="portfolio",
            name="description_en",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="description_ru",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="description_uz",
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="title_en",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="title_ru",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="portfolio",
            name="title_uz",
            field=models.CharField(max_length=250, null=True),
        ),
    ]