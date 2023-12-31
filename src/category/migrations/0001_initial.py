# Generated by Django 4.2.1 on 2023-06-20 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('level', models.CharField(max_length=120)),
                ('school', models.CharField(max_length=200)),
                ('deadline', models.DateField(null=True)),
                ('more_info', models.TextField()),
                ('description', models.TextField(blank=True, max_length=275, null=True)),
                ('link_web', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
    ]
