# Generated by Django 5.1.6 on 2025-02-18 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0006_consumer_created_at_consumer_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='type',
            field=models.CharField(choices=[('Buisness', 'buisness'), ('Customer', 'customer')], default='Customer', max_length=20),
        ),
        migrations.AlterField(
            model_name='seller',
            name='type',
            field=models.CharField(choices=[('Buisness', 'buisness'), ('Customer', 'customer')], default='Customer', max_length=20),
        ),
    ]
