# Generated by Django 4.2.7 on 2024-03-10 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_usuario_apellidos'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='static/profile_images/'),
        ),
    ]