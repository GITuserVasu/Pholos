# Generated by Django 4.1 on 2024-03-11 06:23

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_farm_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='farm_details',
            name='polygon_coordinates',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326),
            preserve_default=False,
        ),
    ]
