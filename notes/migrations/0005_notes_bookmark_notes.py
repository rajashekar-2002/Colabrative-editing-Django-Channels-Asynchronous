# Generated by Django 4.1.7 on 2023-04-07 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_alter_notes_notes_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='bookmark_notes',
            field=models.BooleanField(default=False),
        ),
    ]