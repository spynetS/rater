# Generated by Django 5.1.1 on 2024-10-06 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='friends',
            field=models.ManyToManyField(to='accounts.account'),
        ),
    ]
