# Generated by Django 3.1 on 2020-05-10 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comunaute', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Genre',
            new_name='Categorie',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='genre',
        ),
        migrations.AddField(
            model_name='produit',
            name='categorie',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='comunaute.categorie'),
            preserve_default=False,
        ),
    ]
