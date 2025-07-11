# Generated by Django 5.2.1 on 2025-06-30 12:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebUDH', '0003_usuario_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='almacen',
            field=models.ManyToManyField(null=True, through='WebUDH.Stock', to='WebUDH.almacen'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='usuario',
            field=models.ManyToManyField(null=True, through='WebUDH.Reseña', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('administrador', 'Administrador'), ('hincha', 'Hincha')], default='hincha', max_length=30),
        ),
    ]
