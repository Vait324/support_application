# Generated by Django 3.0.5 on 2022-02-01 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20220201_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('frozen', 'Frozen')], default='open', max_length=30),
        ),
    ]