# Generated by Django 3.1 on 2020-05-11 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunaute', '0003_auto_20200511_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='image',
            field=models.CharField(default='assets/images/logo.png', max_length=50),
            preserve_default=False,
        ),
    ]
