# Generated by Django 4.2.8 on 2024-03-19 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_remove_comment_avatar_comment_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_category',
        ),
    ]