# Generated by Django 2.0.3 on 2018-03-22 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_auto_20180321_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionstatus',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
