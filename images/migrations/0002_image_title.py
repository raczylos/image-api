# Generated by Django 4.2.6 on 2023-10-12 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='title',
            field=models.CharField(default='Untitled', max_length=20),
        ),
    ]
