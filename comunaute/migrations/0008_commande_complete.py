# Generated by Django 3.1 on 2020-05-21 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunaute', '0007_auto_20200511_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='complete',
            field=models.BooleanField(default=True),
        ),
    ]
