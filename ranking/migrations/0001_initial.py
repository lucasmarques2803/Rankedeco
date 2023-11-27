# Generated by Django 3.2.12 on 2023-11-27 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bandeco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bandeco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranking.bandeco')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ranking.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='bandeco',
            field=models.ManyToManyField(through='ranking.Nota', to='ranking.Bandeco'),
        ),
    ]