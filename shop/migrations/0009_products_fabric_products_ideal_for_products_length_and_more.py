# Generated by Django 4.1.2 on 2022-11-03 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0008_remove_offers_img_products_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="fabric",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="products",
            name="ideal_for",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="products",
            name="length",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="products",
            name="occasion",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="products",
            name="pattern",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="products",
            name="sec_color",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="products",
            name="wash_care",
            field=models.CharField(default="", max_length=50),
        ),
    ]
