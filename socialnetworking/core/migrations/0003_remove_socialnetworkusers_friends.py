# Generated by Django 4.0 on 2023-04-02 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_friendsthrough_friend_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialnetworkusers',
            name='friends',
        ),
    ]
