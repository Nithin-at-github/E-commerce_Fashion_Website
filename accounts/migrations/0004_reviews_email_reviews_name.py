# Generated by Django 4.1.2 on 2022-11-29 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_reviews"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviews",
            name="email",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="reviews",
            name="name",
            field=models.CharField(default="", max_length=50),
        ),
    ]