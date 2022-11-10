# Generated by Django 4.1.2 on 2022-10-27 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_products"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brands",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("logo", models.ImageField(upload_to="brands")),
            ],
        ),
        migrations.CreateModel(
            name="Offers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("offer", models.IntegerField()),
                ("expiry", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="SubCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="products",
            name="featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="products",
            name="brand",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.brands",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="offer",
            field=models.ForeignKey(
                blank=True,
                default="",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.offers",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="sub_category",
            field=models.ForeignKey(
                blank=True,
                default="",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="shop.subcategory",
            ),
        ),
    ]