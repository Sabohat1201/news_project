# Generated by Django 4.1.5 on 2023-02-27 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='pdated_time',
            new_name='updated_time',
        ),
    ]
