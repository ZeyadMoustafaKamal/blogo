# Generated by Django 4.2 on 2023-04-12 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_code',
            field=models.CharField(max_length=25),
            preserve_default=False,
        ),
    ]
