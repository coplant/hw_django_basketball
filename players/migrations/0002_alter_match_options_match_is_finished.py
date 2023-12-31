# Generated by Django 4.2.7 on 2023-11-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ('-date', 'is_finished')},
        ),
        migrations.AddField(
            model_name='match',
            name='is_finished',
            field=models.BooleanField(default=0, verbose_name='Игра состоялась'),
        ),
    ]
