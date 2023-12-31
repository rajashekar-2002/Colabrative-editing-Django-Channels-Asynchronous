# Generated by Django 4.1.7 on 2023-06-10 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('signin', '0002_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grpname', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(default=None, max_length=50)),
                ('createdby', models.EmailField(default='@gmail.com', max_length=254)),
                ('date', models.DateTimeField(auto_now=True)),
                ('participants', models.TextField(default=None)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='signin.user')),
            ],
        ),
        migrations.CreateModel(
            name='Collabnote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('group', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='collabrate1.group')),
            ],
        ),
    ]
