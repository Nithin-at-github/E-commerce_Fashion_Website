# Generated by Django 4.1.2 on 2022-10-28 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0003_brands_offers_subcategory_products_featured_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="img",
            field=models.ImageField(default="", upload_to="categ"),
        ),
        migrations.AddField(
            model_name="offers",
            name="img",
            field=models.ImageField(default="", upload_to="offers"),
        ),
        migrations.AddField(
            model_name="products",
            name="img1",
            field=models.ImageField(default="", upload_to="products"),
        ),
        migrations.AddField(
            model_name="products",
            name="img2",
            field=models.ImageField(default="", upload_to="products"),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="desc",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="subcategory",
            name="img",
            field=models.ImageField(default="", upload_to="subcat"),
        ),
    ]
