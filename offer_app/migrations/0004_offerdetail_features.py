# Generated by Django 5.1.6 on 2025-02-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer_app', '0003_offerdetail_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerdetail',
            name='features',
            field=models.JSONField(default=list),
        ),
    ]
