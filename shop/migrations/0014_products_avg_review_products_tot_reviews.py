# Generated by Django 4.1.2 on 2022-11-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0013_remove_products_stock_products_stock_l_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="avg_review",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="products",
            name="tot_reviews",
            field=models.IntegerField(default=0),
        ),
    ]
