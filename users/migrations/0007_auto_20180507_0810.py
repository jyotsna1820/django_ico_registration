# Generated by Django 2.0 on 2018-05-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20180507_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='eth_address',
            field=models.CharField(blank=True, max_length=42, null=True, unique=True),
        ),
    ]
