# Generated by Django 4.2.3 on 2023-10-24 03:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0015_alter_order_paymentstatus"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="code",
            field=models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True),
        ),
    ]
