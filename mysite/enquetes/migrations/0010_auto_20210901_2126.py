# Generated by Django 2.2.7 on 2021-09-01 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enquetes', '0009_perfil_autor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='perfil',
            options={'verbose_name_plural': 'Informações de Perfil'},
        ),
        migrations.AddField(
            model_name='autor',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='rotulos',
            field=models.ManyToManyField(to='enquetes.Rotulo', verbose_name='Rótulos'),
        ),
    ]
