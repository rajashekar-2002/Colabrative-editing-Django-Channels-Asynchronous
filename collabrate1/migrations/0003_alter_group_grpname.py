# Generated by Django 4.1.7 on 2023-06-11 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collabrate1', '0002_collabnote_user_alter_group_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='grpname',
            field=models.CharField(max_length=20),
        ),
    ]
