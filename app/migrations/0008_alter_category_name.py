# Generated by Django 4.1.7 on 2024-07-06 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_rename_email_address_post_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='', help_text='name of catygory', max_length=50, verbose_name='name'),
        ),
    ]
