# Generated by Django 2.0 on 2018-01-05 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Railapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='station_id',
            field=models.CharField(max_length=120, primary_key=True, serialize=False),
        ),
    ]
