# Generated by Django 2.2.16 on 2022-04-27 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220428_0144'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='title',
            name='unique_title',
        ),
        migrations.AddConstraint(
            model_name='title',
            constraint=models.UniqueConstraint(fields=('name', 'year'), name='unique_title'),
        ),
    ]
