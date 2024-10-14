# Generated by Django 5.0.7 on 2024-10-13 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dataanalytics",
            name="top_customer",
        ),
        migrations.RemoveField(
            model_name="dataanalytics",
            name="top_selling_product",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="employee",
        ),
        migrations.DeleteModel(
            name="ExpenseReport",
        ),
        migrations.RemoveField(
            model_name="product",
            name="supplier",
        ),
        migrations.DeleteModel(
            name="RevenueReport",
        ),
        migrations.DeleteModel(
            name="Customer",
        ),
        migrations.DeleteModel(
            name="DataAnalytics",
        ),
        migrations.DeleteModel(
            name="Employee",
        ),
        migrations.DeleteModel(
            name="Shift",
        ),
        migrations.DeleteModel(
            name="Product",
        ),
        migrations.DeleteModel(
            name="Supplier",
        ),
    ]