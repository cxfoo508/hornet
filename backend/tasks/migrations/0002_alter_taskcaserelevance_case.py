# Generated by Django 4.0.6 on 2022-08-08 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcaserelevance',
            name='case',
            field=models.TextField(default='', null=True, verbose_name='case'),
        ),
    ]
