# Generated by Django 2.0.3 on 2018-06-20 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20180620_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='user_stage',
            field=models.CharField(choices=[('G', 'GRADUATED'), ('U', 'UNGRADUATED'), ('I', 'IN CLASS'), ('N', 'NOT STUDENT')], default='N', max_length=1),
        ),
    ]
