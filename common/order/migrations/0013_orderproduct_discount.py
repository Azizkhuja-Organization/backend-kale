# Generated by Django 4.2.3 on 2023-09-03 07:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0012_alter_order_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderproduct",
            name="discount",
            field=models.FloatField(default=0),
        ),
    ]