# Generated by Django 2.2.7 on 2021-08-18 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enquetes', '0004_auto_20210818_1300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pergunta',
            old_name='usuario',
            new_name='autor',
        ),
    ]
