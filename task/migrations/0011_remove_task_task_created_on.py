# Generated by Django 4.1.7 on 2023-04-02 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_remove_task_time_diff_task_task_created_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='task_created_on',
        ),
    ]
