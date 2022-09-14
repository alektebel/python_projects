# Generated by Django 4.0.4 on 2022-04-25 12:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labeling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datas',
            name='props',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), default=[0.5, 0.5], size=2),
            preserve_default=False,
        ),
    ]
