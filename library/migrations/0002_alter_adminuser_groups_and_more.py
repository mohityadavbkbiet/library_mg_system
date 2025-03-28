# Generated by Django 4.2 on 2025-03-22 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='admin_users', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='admin_users_permissions', to='auth.permission'),
        ),
    ]
