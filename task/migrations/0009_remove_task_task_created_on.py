# Generated by Django 4.1.7 on 2023-04-02 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_alter_task_task_created_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_created_on',
        ),
    ]
