# Generated by Django 5.1.1 on 2024-12-05 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizards', '0010_delete_wizard_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
