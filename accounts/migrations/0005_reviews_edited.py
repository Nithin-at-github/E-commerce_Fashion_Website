# Generated by Django 4.1.2 on 2022-11-30 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_reviews_email_reviews_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviews",
            name="edited",
            field=models.BooleanField(default=False),
        ),
    ]
