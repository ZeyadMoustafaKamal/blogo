# Generated by Django 4.2 on 2023-06-01 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_user_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_code',
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_stuff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
    ]
