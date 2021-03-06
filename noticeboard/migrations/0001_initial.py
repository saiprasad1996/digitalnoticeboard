# Generated by Django 2.1.5 on 2020-12-28 02:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('notice_text', models.TextField()),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2020, 12, 28, 7, 47, 37, 280208))),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noticeboard.Department')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('designation', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=80)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noticeboard.Department')),
            ],
        ),
        migrations.AddField(
            model_name='posts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='noticeboard.User'),
        ),
    ]
