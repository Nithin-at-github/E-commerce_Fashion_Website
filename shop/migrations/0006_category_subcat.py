# Generated by Django 4.1.2 on 2022-10-29 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_ads_products_info"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="subcat",
            field=models.ManyToManyField(to="shop.subcategory"),
        ),
    ]
