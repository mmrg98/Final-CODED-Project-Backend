# Generated by Django 3.1.3 on 2020-11-30 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fammunity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.ImageField(null=True, upload_to='brand_logos'),
        ),
    ]
