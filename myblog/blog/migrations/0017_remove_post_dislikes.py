# Generated by Django 4.2.8 on 2024-01-08 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_post_dislikes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dislikes',
        ),
    ]
