# Generated by Django 4.2.6 on 2023-11-30 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ranking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comentario",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]