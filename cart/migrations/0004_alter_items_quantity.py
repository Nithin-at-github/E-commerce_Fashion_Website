# Generated by Django 4.1.2 on 2022-11-08 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_items_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="items",
            name="quantity",
            field=models.CharField(max_length=10),
        ),
    ]