# Generated by Django 4.0 on 2023-04-02 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_friendsthrough_unique_social_friend_relation_and_more'),
    ]

    operations = [
        # migrations.RemoveConstraint(
        #     model_name='friendsthrough',
        #     name='unique_social_friend_relation',
        # ),
        # migrations.AddConstraint(
        #     model_name='friendsthrough',
        #     constraint=models.UniqueConstraint(fields=('social_network_user', 'friend', 'relationship_type'), name='unique_social_friend_relation'),
        # ),
    ]