# Generated by Django 4.1.2 on 2022-12-01 15:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_reviews_last_updated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviews",
            name="last_updated",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
