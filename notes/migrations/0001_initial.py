# Generated by Django 4.1.7 on 2023-03-22 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notebook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes_name', models.CharField(max_length=20)),
                ('notes_text', models.TextField(default='text here...')),
                ('notes_created_on', models.DateTimeField(auto_now_add=True)),
                ('notes_last_modified', models.DateTimeField(auto_now=True)),
                ('tags', models.TextField(blank=True, default='none', max_length=50)),
                ('notebook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='notebook.notebook')),
            ],
        ),
    ]