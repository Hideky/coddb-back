# Generated by Django 4.2.3 on 2023-08-06 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_rarity_artifact_quality'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artifact',
            old_name='categorie_1',
            new_name='category_1',
        ),
        migrations.RenameField(
            model_name='artifact',
            old_name='categorie_2',
            new_name='category_2',
        ),
        migrations.RenameField(
            model_name='artifact',
            old_name='categorie_3',
            new_name='category_3',
        ),
    ]
