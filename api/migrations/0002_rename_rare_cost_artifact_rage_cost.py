# Generated by Django 4.2.3 on 2023-08-05 02:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artifact',
            old_name='rare_cost',
            new_name='rage_cost',
        ),
    ]
