# Generated by Django 5.1.6 on 2025-02-18 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0015_consumer_type_seller_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='type',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='seller',
            name='type',
            field=models.CharField(max_length=20),
        ),
    ]
