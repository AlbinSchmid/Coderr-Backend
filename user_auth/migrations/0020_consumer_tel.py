# Generated by Django 5.1.6 on 2025-02-19 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0019_remove_seller_description_remove_seller_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='tel',
            field=models.CharField(default='', max_length=255),
        ),
    ]
