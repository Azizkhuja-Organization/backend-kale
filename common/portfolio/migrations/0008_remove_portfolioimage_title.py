# Generated by Django 4.2.3 on 2023-11-01 18:15

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0007_portfolio_logo_portfolioimage_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="portfolioimage",
            name="title",
        ),
    ]
