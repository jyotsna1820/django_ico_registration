# Generated by Django 2.0 on 2018-05-06 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180506_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='eth_address',
            field=models.CharField(max_length=42, null=True, unique=True),
        ),
    ]
