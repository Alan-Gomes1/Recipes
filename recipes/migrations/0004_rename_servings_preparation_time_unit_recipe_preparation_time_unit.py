# Generated by Django 4.1.7 on 2023-04-02 00:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_preparation_time_unit_recipe_servings_preparation_time_unit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='servings_preparation_time_unit',
            new_name='preparation_time_unit',
        ),
    ]