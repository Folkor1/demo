# Generated by Django 4.2.7 on 2024-02-11 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bookings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("lesson", models.CharField(max_length=50)),
                ("lesson_type", models.CharField(max_length=50)),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("status", models.BooleanField(default=False)),
                (
                    "confirmed",
                    models.CharField(
                        choices=[
                            ("Confirmed", "Confirmed"),
                            ("Pending", "Pending"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="Pending",
                        max_length=50,
                    ),
                ),
                (
                    "datetime_booked",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "finalized",
                    models.CharField(
                        choices=[
                            ("Not finalized", "Not finalized"),
                            ("Discarded", "Discarded"),
                            ("Finalized", "Finalized"),
                        ],
                        default="Not finalized",
                        max_length=50,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                ("comms", models.TextField(blank=True)),
                ("flagged", models.BooleanField(blank=True, default=False)),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Booking",
                "verbose_name_plural": "Bookings",
                "ordering": ["-date"],
            },
        ),
    ]