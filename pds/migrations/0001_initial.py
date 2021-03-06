# Generated by Django 3.0.5 on 2020-12-01 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FCI_regional_office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office_name', models.CharField(max_length=200)),
                ('office_Lat', models.FloatField(default=0)),
                ('office_Long', models.FloatField(default=0)),
                ('office_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='godowns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('godowns_name', models.CharField(max_length=200)),
                ('godowns_Lat', models.FloatField(default=0)),
                ('godowns_Long', models.FloatField(default=0)),
                ('godowns_number', models.IntegerField(default=0)),
            ],
        ),
    ]
