# Generated by Django 5.0.7 on 2024-08-08 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalogue", "0002_alter_category_options_brand_created_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brand",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalogue.brand",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="catalogue.category",
            ),
        ),
    ]