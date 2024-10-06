# Generated by Django 5.1.1 on 2024-10-06 08:12

import django.db.models.deletion
import extensions.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_profile_username_alter_user_is_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Delete post?')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Delete time')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update time')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Delete post?')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='Delete time')),
                ('image', models.ImageField(blank=True, default='default/default-post.png', null=True, upload_to=extensions.utils.upload_file_path, verbose_name='Image')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField()),
                ('slug', models.SlugField(blank=True, help_text='Do not fill in here', unique=True, verbose_name='Slug')),
                ('visits', models.PositiveIntegerField(default=0, verbose_name='Visits')),
                ('published_status', models.CharField(blank=True, choices=[('p', 'publish'), ('d', 'draft')], max_length=1, null=True, verbose_name='Status')),
                ('published_at', models.DateTimeField(verbose_name='Publish time')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile', verbose_name='Author')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.category')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-published_at'],
            },
        ),
    ]
