# Generated by Django 4.1.2 on 2022-11-14 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0006_items_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="Orders",
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
                ("tot_amount", models.FloatField()),
                ("firstname", models.CharField(max_length=50)),
                ("lastname", models.CharField(blank=True, max_length=50)),
                ("email", models.CharField(max_length=50)),
                ("mob_no", models.CharField(max_length=10)),
                ("address_line1", models.CharField(max_length=50)),
                ("address_line2", models.CharField(max_length=50)),
                ("city", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=50)),
                ("country", models.CharField(max_length=50)),
                ("zip_code", models.CharField(max_length=6)),
                ("payment_type", models.CharField(max_length=50)),
                ("status", models.CharField(max_length=50)),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cart.cartlist"
                    ),
                ),
                ("items", models.ManyToManyField(to="cart.items")),
            ],
        ),
    ]
