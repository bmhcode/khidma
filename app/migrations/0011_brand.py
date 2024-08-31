# Generated by Django 5.1 on 2024-08-30 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_wishlist_model_options_alter_postimages_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name of brand')),
                ('image', models.ImageField(blank=True, default='brand.jpg', upload_to='brand', verbose_name='brand')),
                ('start', models.DateTimeField(verbose_name='Start at')),
                ('end', models.DateTimeField(verbose_name='End at')),
                ('is_active', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
    ]
