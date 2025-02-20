# Generated by Django 5.1.1 on 2024-11-27 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizards', '0007_alter_order_team_alter_wizard_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Новый', 'New'), ('В процессе', 'In Progress'), ('Выполнен', 'Completed'), ('Невыполнен', 'Failed')], default='Новый', max_length=20, verbose_name='Статус'),
        ),
    ]
