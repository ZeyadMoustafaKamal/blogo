# Generated by Django 4.2 on 2023-05-01 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_alter_blog_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='members',
        ),
        migrations.DeleteModel(
            name='BlogMemberRelationship',
        ),
    ]
