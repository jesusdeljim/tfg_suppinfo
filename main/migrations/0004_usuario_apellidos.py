# Generated by Django 4.2.7 on 2024-03-10 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_categoria_slug_subcategoria_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='apellidos',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
