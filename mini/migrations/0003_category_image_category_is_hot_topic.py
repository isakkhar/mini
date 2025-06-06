# Generated by Django 5.2.1 on 2025-05-28 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini', '0002_education_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categories/'),
        ),
        migrations.AddField(
            model_name='category',
            name='is_hot_topic',
            field=models.BooleanField(default=False),
        ),
    ]
