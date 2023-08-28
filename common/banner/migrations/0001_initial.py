# Generated by Django 4.2.3 on 2023-08-28 11:21

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Banner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("photo", models.ImageField(upload_to="bannerImage", verbose_name="Image of Banner")),
                ("url", models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="PointerNumber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("client", models.CharField(max_length=20)),
                ("product", models.CharField(max_length=20)),
                ("project", models.CharField(max_length=20)),
                ("delivered", models.CharField(max_length=20)),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
        migrations.CreateModel(
            name="SmallBanner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guid", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("photo", models.ImageField(upload_to="smallBannerImage", verbose_name="Image of SmallBanner")),
                ("url", models.CharField(blank=True, max_length=250, null=True)),
            ],
            options={
                "ordering": ["-id"],
            },
        ),
    ]
