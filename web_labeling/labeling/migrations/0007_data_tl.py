# Generated by Django 4.0.4 on 2022-04-29 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labeling', '0006_rename_datatest_labeltest_remain_datatest'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='tl',
            field=models.TextField(default='class_name', max_length=30),
        ),
    ]
