# Generated by Django 5.0.6 on 2024-06-01 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_friends_friendrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id']},
        ),
    ]
