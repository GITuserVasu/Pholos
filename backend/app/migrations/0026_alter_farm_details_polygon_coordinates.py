# Generated by Django 4.1 on 2024-03-11 06:24

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_farm_details_polygon_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm_details',
            name='polygon_coordinates',
            field=django.contrib.gis.db.models.fields.PolygonField(null=True, srid=4326),
        ),
    ]
