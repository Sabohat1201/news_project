# Generated by Django 4.1.5 on 2023-04-30 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
