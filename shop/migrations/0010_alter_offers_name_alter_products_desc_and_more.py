# Generated by Django 4.1.2 on 2022-11-03 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0009_products_fabric_products_ideal_for_products_length_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offers",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="products",
            name="desc",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="products",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]