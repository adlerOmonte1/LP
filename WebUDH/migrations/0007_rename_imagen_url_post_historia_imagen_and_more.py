# Generated by Django 5.2.1 on 2025-07-07 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebUDH', '0006_rename_contenido_noticia_descripcion_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post_historia',
            old_name='imagen_url',
            new_name='imagen',
        ),
        migrations.AlterField(
            model_name='post_historia',
            name='fecha_publicacion',
            field=models.DateField(auto_now_add=True),
        ),
    ]
