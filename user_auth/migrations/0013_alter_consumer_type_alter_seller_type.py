# Generated by Django 5.1.6 on 2025-02-18 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0012_delete_testmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='type',
            field=models.CharField(choices=[('buisness', 'Buisness'), ('customer', 'Customer')], max_length=20),
        ),
        migrations.AlterField(
            model_name='seller',
            name='type',
            field=models.CharField(choices=[('buisness', 'Buisness'), ('customer', 'Customer')], max_length=20),
        ),
    ]
