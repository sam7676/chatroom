# Generated by Django 4.1.4 on 2023-01-15 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatroom_app', '0004_userlist_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chats',
            name='time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='serverlist',
            name='lastUpdate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='userlist',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
