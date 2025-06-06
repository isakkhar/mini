# Generated by Django 5.2.1 on 2025-05-28 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=200)),
                ('institution', models.CharField(max_length=200)),
                ('start_year', models.CharField(max_length=10)),
                ('end_year', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
                ('start_year', models.CharField(max_length=10)),
                ('end_year', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
