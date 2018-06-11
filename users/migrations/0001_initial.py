# Generated by Django 2.0 on 2018-04-19 06:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('eth_address', models.CharField(max_length=42)),
                ('eth_amount', models.DecimalField(decimal_places=10, default=0.1, max_digits=20, validators=[django.core.validators.MinValueValidator(0.1, message='ETH amount should minimum 0.1')])),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Registered'), (2, 'Pending'), (3, 'Unconfirmed')], default=2)),
                ('country', models.CharField(choices=[('canada', 'CANADA')], default='canada', max_length=50)),
                ('editable', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]