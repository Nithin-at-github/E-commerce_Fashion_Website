# Generated by Django 4.1.2 on 2022-11-03 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0007_alter_category_subcat"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="offers",
            name="img",
        ),
        migrations.AddField(
            model_name="products",
            name="color",
            field=models.CharField(default="", max_length=50),
        ),
    ]