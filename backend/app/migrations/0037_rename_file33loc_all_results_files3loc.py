# Generated by Django 4.1 on 2024-03-27 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_remove_all_results_files3loc_all_results_file33loc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='all_results',
            old_name='file33loc',
            new_name='files3loc',
        ),
    ]
