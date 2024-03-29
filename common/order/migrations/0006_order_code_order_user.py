# Generated by Django 4.2.3 on 2023-08-17 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0005_orderproduct_rename_isdelivery_order_installation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="code",
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orderUser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
