# Generated by Django 2.2.7 on 2021-06-23 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enquetes', '0002_pergunta_autor'),
    ]

    operations = [
        migrations.AddField(
            model_name='pergunta',
            name='data_encerramento',
            field=models.DateField(null=True, verbose_name='Data de Encerramento'),
        ),
    ]
