# Generated by Django 2.0.3 on 2018-06-20 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20180607_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='user_stage',
            field=models.CharField(choices=[('G', 'GRADUATED'), ('R', 'RETAKE'), ('U', 'UNGRADUATED'), ('I', 'IN CLASS'), ('N', 'NOT STUDENT')], default='N', max_length=1),
        ),
    ]
