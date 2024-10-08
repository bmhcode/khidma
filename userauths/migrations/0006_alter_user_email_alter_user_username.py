# Generated by Django 4.1.7 on 2024-07-04 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0005_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
