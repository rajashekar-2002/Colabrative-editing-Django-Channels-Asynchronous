# Generated by Django 4.1.7 on 2023-04-27 04:26

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signin', '0002_alter_user_email'),
        ('notebook', '0008_alter_shared_with_me_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shared_with_me',
            name='notebook_slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='notebook_name'),
        ),
        migrations.AlterField(
            model_name='shared_with_me',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='signin.user'),
        ),
    ]