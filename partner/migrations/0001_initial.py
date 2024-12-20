# Generated by Django 5.1.3 on 2024-11-28 09:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("catalogue", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Partner",
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
                ("name", models.CharField(max_length=32)),
                ("is_active", models.BooleanField()),
                ("created_time", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="PartnerProduct",
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
                ("price", models.PositiveBigIntegerField(default=0)),
                ("created_time", models.DateTimeField(auto_now=True)),
                (
                    "partner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="partner.partner",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="partners",
                        to="catalogue.product",
                    ),
                ),
            ],
        ),
    ]
