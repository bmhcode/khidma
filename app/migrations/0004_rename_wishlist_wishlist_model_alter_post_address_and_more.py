# Generated by Django 4.1.7 on 2024-06-02 13:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_post_tags'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wishlist',
            new_name='Wishlist_model',
        ),
        migrations.AlterField(
            model_name='post',
            name='address',
            field=models.CharField(default='', help_text='Address of post', max_length=200, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, default='', help_text='Informations about your post', null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='email_address',
            field=models.EmailField(blank=True, default='', help_text='yourmail@gmail.com', max_length=255, null=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='', help_text='Title of post', max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='postimages',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='images of post'),
        ),
    ]
