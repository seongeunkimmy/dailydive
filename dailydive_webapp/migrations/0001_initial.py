# Generated by Django 3.2 on 2023-07-04 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='solutions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sentiment', models.CharField(max_length=200)),
                ('solution_title', models.CharField(max_length=200)),
                ('solution_guide', models.CharField(max_length=200)),
                ('img_url', models.CharField(max_length=200)),
            ],
        ),
    ]
